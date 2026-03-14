### subscription.py
### Entity class for Subscription


class Subscription:

    def __init__(self, subscription_id, customer_name, email,
                 plan_type, start_date, end_date, monthly_fee, is_active):
        self.__subscription_id = subscription_id
        self.__customer_name   = customer_name
        self.__email           = email
        self.__plan_type       = plan_type      # 'Basic', 'Standard', 'Premium'
        self.__start_date      = start_date     # datetime.date object
        self.__end_date        = end_date       # datetime.date object
        self.__monthly_fee     = monthly_fee    # float
        self.__is_active       = is_active      # int: 1 = Active, 0 = Inactive

    def get_subscription_id(self):
        return self.__subscription_id

    def set_subscription_id(self, subscription_id):
        self.__subscription_id = subscription_id

    def get_customer_name(self):
        return self.__customer_name

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_plan_type(self):
        return self.__plan_type

    def set_plan_type(self, plan_type):
        self.__plan_type = plan_type

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_monthly_fee(self):
        return self.__monthly_fee

    def set_monthly_fee(self, monthly_fee):
        self.__monthly_fee = monthly_fee

    def get_is_active(self):
        return self.__is_active

    def set_is_active(self, is_active):
        self.__is_active = is_active
