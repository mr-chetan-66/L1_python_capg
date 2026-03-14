### rental.py
### Entity class for Rental

class Rental:
    def __init__(self, rental_id, customer_id, vehicle_id, start_date,
                 end_date, daily_rate, total_amount, payment_status):
        self.__rental_id      = rental_id
        self.__customer_id    = customer_id
        self.__vehicle_id     = vehicle_id
        self.__start_date     = start_date
        self.__end_date       = end_date
        self.__daily_rate     = daily_rate
        self.__total_amount   = total_amount
        self.__payment_status = payment_status

    def get_rental_id(self):
        return self.__rental_id

    def set_rental_id(self, rental_id):
        self.__rental_id = rental_id

    def get_customer_id(self):
        return self.__customer_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def get_vehicle_id(self):
        return self.__vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.__vehicle_id = vehicle_id

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_daily_rate(self):
        return self.__daily_rate

    def set_daily_rate(self, daily_rate):
        self.__daily_rate = daily_rate

    def get_total_amount(self):
        return self.__total_amount

    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount

    def get_payment_status(self):
        return self.__payment_status

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status
