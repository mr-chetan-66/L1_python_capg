from datetime import date, datetime

class Car:
    def __init__(self, rental_id, car_number, customer_name,
                 basic_cost: float, no_of_days: int,
                 rental_date: date, total_amount: float):
        self._rental_id = rental_id
        self._car_number = car_number
        self._customer_name = customer_name
        self._basic_cost = float(basic_cost)
        self._no_of_days = int(no_of_days)
        self._rental_date = rental_date
        self._total_amount = float(total_amount)

    # ---- Getters ----
    def get_rental_id(self):
        return self._rental_id

    def get_car_number(self):
        return self._car_number

    def get_customer_name(self):
        return self._customer_name

    def get_basic_cost(self):
        return self._basic_cost

    def get_no_of_days(self):
        return self._no_of_days

    def get_rental_date(self):
        return self._rental_date

    def get_total_amount(self):
        return self._total_amount

    # ---- Setters ----
    def set_rental_id(self, rental_id):
        self._rental_id = rental_id

    def set_car_number(self, car_number):
        self._car_number = car_number

    def set_customer_name(self, customer_name):
        self._customer_name = customer_name

    def set_basic_cost(self, basic_cost: float):
        self._basic_cost = float(basic_cost)

    def set_no_of_days(self, no_of_days: int):
        self._no_of_days = int(no_of_days)

    def set_rental_date(self, rental_date: date):
        self._rental_date = rental_date

    def set_total_amount(self, total_amount: float):
        self._total_amount = float(total_amount)
        
    def calculate_total_amount(self):
        total=self._basic_cost*self._no_of_days
        dis=0
        if self._no_of_days>3:
            dis=0.02*total
            
        elif self._no_of_days>1:
            dis=0.04*total
            
        total-=dis   
        self._total_amount=total
        return dis

            