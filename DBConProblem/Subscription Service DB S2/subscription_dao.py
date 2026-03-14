### subscription_dao.py
### Data Access Object Class — all DB operations for Subscription
### Class-based DAO with SELECT, UPDATE operations and ordered validation

import subscription as sb
import cx_Oracle
from datetime import date
from dateutil.relativedelta import relativedelta


# Custom Exceptions — defined here as they are raised inside the DAO
class InvalidPlanTypeException(Exception):
    pass

class SubscriptionNotFoundException(Exception):
    pass

class SubscriptionAlreadyActiveException(Exception):
    pass

class SubscriptionInactiveException(Exception):
    pass


# Valid plan types and their monthly fees
PLAN_FEES = {
    'basic'    : 199.0,
    'standard' : 499.0,
    'premium'  : 999.0
}


class SubscriptionDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve a single subscription by subscription_id
    # ----------------------------------------------------------------
    def retrieve_subscription_by_id(self, subscription_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT subscription_id, customer_name, email, plan_type,
                   start_date, end_date, monthly_fee, is_active
            FROM subscription
            WHERE subscription_id = :1
        """

        cursor.execute(query, (subscription_id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        s_date = row[4].date() if hasattr(row[4], 'date') else row[4]
        e_date = row[5].date() if hasattr(row[5], 'date') else row[5]

        return sb.Subscription(row[0], row[1], row[2], row[3],
                               s_date, e_date, float(row[6]), row[7])

    # ----------------------------------------------------------------
    # SELECT — retrieve all subscriptions for a given plan type
    #          validates plan type first, raises custom exception if empty
    # ----------------------------------------------------------------
    def retrieve_subscriptions_by_plan(self, plan_type):
        # Step 1: Validate plan type before hitting the DB
        if plan_type.lower() not in PLAN_FEES:
            raise InvalidPlanTypeException(
                "Invalid plan type. Choose from Basic, Standard, or Premium."
            )

        cursor = self.__conn.cursor()

        query = """
            SELECT subscription_id, customer_name, email, plan_type,
                   start_date, end_date, monthly_fee, is_active
            FROM subscription
            WHERE LOWER(plan_type) = :1
            ORDER BY end_date ASC
        """

        cursor.execute(query, (plan_type.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        # Step 2: Raise exception if no records found for a valid plan
        if not rows:
            raise SubscriptionNotFoundException(
                "No subscriptions found for the given plan type."
            )

        subscription_list = []
        for row in rows:
            s_date = row[4].date() if hasattr(row[4], 'date') else row[4]
            e_date = row[5].date() if hasattr(row[5], 'date') else row[5]
            obj = sb.Subscription(row[0], row[1], row[2], row[3],
                                  s_date, e_date, float(row[6]), row[7])
            subscription_list.append(obj)

        return subscription_list

    # ----------------------------------------------------------------
    # UPDATE — renew a subscription by extending its end_date
    #          validates in exact order: exists → active → months range
    # ----------------------------------------------------------------
    def renew_subscription(self, subscription_id, renewal_months):
        # Step 1: Check if subscription exists
        subscription = self.retrieve_subscription_by_id(subscription_id)

        if subscription is None:
            raise SubscriptionNotFoundException(
                "Subscription not found for the given ID."
            )

        # Step 2: Check if subscription is active
        if subscription.get_is_active() != 1:
            raise SubscriptionInactiveException(
                "Cannot renew an inactive subscription."
            )

        # Step 3: Validate renewal months range
        if not (1 <= renewal_months <= 12):
            raise InvalidPlanTypeException(
                "Renewal period must be between 1 and 12 months."
            )

        # Calculate new end date using month-accurate relativedelta
        current_end  = subscription.get_end_date()
        monthly_fee  = subscription.get_monthly_fee()
        new_end_date = current_end + relativedelta(months=renewal_months)
        total_cost   = round(renewal_months * monthly_fee, 2)

        # Update end_date in DB and commit
        try:
            cursor = self.__conn.cursor()

            update_query = """
                UPDATE subscription
                SET end_date = :1
                WHERE subscription_id = :2
            """

            cursor.execute(update_query, (new_end_date, subscription_id))
            self.__conn.commit()
            cursor.close()

        except cx_Oracle.DatabaseError:
            self.__conn.rollback()
            return None

        return (new_end_date, total_cost)

    # ----------------------------------------------------------------
    # SELECT — calculate total monthly revenue grouped by plan type
    #          only from active subscriptions (is_active = 1)
    # ----------------------------------------------------------------
    def calculate_total_revenue_by_plan(self):
        # Initialise all three plans to 0.0 before querying
        revenue = {'Basic': 0.0, 'Standard': 0.0, 'Premium': 0.0}

        cursor = self.__conn.cursor()

        query = """
            SELECT plan_type, SUM(monthly_fee)
            FROM subscription
            WHERE is_active = 1
            GROUP BY plan_type
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        for row in rows:
            plan = row[0].title()
            if plan in revenue:
                revenue[plan] = round(float(row[1]), 2)

        return revenue
