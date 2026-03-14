### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import subscription_dao as dao_module
import subscription_util as util
from subscription_dao import (InvalidPlanTypeException,
                               SubscriptionNotFoundException,
                               SubscriptionAlreadyActiveException,
                               SubscriptionInactiveException)


def main():
    conn             = db.get_connection()
    subscription_dao = dao_module.SubscriptionDao(conn)

    print("=" * 55)
    print("       SUBSCRIPTION SERVICE MANAGEMENT SYSTEM")
    print("=" * 55)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve and display subscriptions by plan type
    # ----------------------------------------------------------------
    print("\n--- VIEW SUBSCRIPTIONS BY PLAN ---")

    plan_type = input("Enter Plan Type (Basic / Standard / Premium) : ")

    try:
        subscriptions = subscription_dao.retrieve_subscriptions_by_plan(plan_type)
    except InvalidPlanTypeException as e:
        print(e)
        return
    except SubscriptionNotFoundException as e:
        print(e)
        return

    # Group by expiry status and display
    grouped = util.group_subscriptions_by_expiry_status(subscriptions)

    print(f"\nSubscription Report - {plan_type.title()} Plan")
    print("=" * 55)

    for status, subs in grouped.items():
        print(f"\n[{status}] - {len(subs)} subscription(s)")
        for s in subs:
            days = util.get_days_remaining(s.get_end_date())
            print(f"  ID       : {s.get_subscription_id()}")
            print(f"  Customer : {s.get_customer_name()}")
            print(f"  Email    : {s.get_email()}")
            print(f"  End Date : {s.get_end_date().strftime('%d-%m-%Y')}")
            print(f"  Days     : {days}")
            print(f"  Status   : {util.get_status_label(s)}")
            print()

    print("Total Subscriptions :", util.get_result_count(subscriptions))
    print("Active Count        :", util.get_active_count(subscriptions))
    print("Alerts Required     :", util.get_non_active_count(subscriptions))

    # ----------------------------------------------------------------
    # STEP 2 — Show total monthly revenue by plan (active subs only)
    # ----------------------------------------------------------------
    print("\n--- MONTHLY REVENUE BY PLAN ---")

    revenue = subscription_dao.calculate_total_revenue_by_plan()
    print("Monthly Revenue by Plan (Active Subscriptions):")
    print("-" * 40)
    for plan, amount in revenue.items():
        print(f"  {plan:<12}: Rs. {amount}")

    # ----------------------------------------------------------------
    # STEP 3 — Renew a subscription
    # ----------------------------------------------------------------
    print("\n--- RENEW A SUBSCRIPTION ---")

    try:
        sub_id         = int(input("Enter Subscription ID to Renew (0 to skip) : "))

        if sub_id != 0:
            if not util.is_valid_subscription_id(sub_id):
                print("Invalid Subscription ID")
                return

            renewal_months = int(input("Enter Number of Months to Renew (1-12)     : "))

            result = subscription_dao.renew_subscription(sub_id, renewal_months)

            if result is None:
                print("Renewal Failed Due to Database Error")
                return

            new_end, cost = result
            print("Renewal Successful!")
            print(f"New End Date     : {new_end.strftime('%d-%m-%Y')}")
            print(f"Renewal Cost     : Rs. {cost}")

    except InvalidPlanTypeException as e:
        print(e)
        return
    except SubscriptionNotFoundException as e:
        print(e)
        return
    except SubscriptionInactiveException as e:
        print(e)
        return
    except ValueError:
        print("Invalid input. Please enter valid values.")
        return

    # ----------------------------------------------------------------
    # STEP 4 — Export expiry alert report to file
    # ----------------------------------------------------------------
    print("\n--- EXPORT EXPIRY ALERT REPORT ---")

    filename = input("Enter Filename to Export (e.g. alerts.txt) : ")

    try:
        util.export_expiry_alert_report(subscriptions, filename)
        print(f"Expiry alert report exported to {filename}")
    except IOError as e:
        print(f"Export Failed: {e}")


if __name__ == '__main__':
    main()
