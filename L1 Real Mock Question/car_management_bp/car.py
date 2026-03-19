# Please do not change the skelecton code given here.
# Write your code only in the provided places alone
from datetime import date
class Car:
    
    # Define the arguments parameterized constructor here
    def __init__(self, rental_id :str,car_number :str,customer_name :str, basic_cost:float, no_of_days:int, rental_date:date):
        self.__rental_id=rental_id
        self.__car_number=car_number
        self.__customer_name=customer_name
        self.__basic_cost=basic_cost
        self.__no_of_days=no_of_days
        self.__rental_date=rental_date
        self.__total_amount=0.0

    def get_rental_id(self):
        return self.__rental_id
    
    def get_car_number(self):
        return self.__car_number
        
    def get_customer_name(self):
        return self.__customer_name
        
    def get_basic_cost(self):
        return self.__basic_cost
        
    def get_no_of_days(self):
        return self.__no_of_days
        
    def get_rental_date(self):
        return self.__rental_date
        
    def get_total_amount(self):
        return self.__total_amount
        
    def set_rental_id(self,rental_id):
        self.__rental_id=rental_id
        
    def set_car_number(self,car_number):
        self.__car_number=car_number
        
    def set_customer_name(self,customer_name):
        self.__customer_name=customer_name
        
    def set_basic_cost(self,basic_cost):
        self.__basic_cost=basic_cost
        
    def set_no_of_days(self,no_of_days):
        self.__no_of_days=no_of_days
    
    def set_rental_date(self,rental_date):
        self.__rental_date=rental_date
        
    def set_total_amount(self,total_amount):
        self.__total_amount=total_amount
    
    
    def calculate_total_amount(self):
        # Write the code here
        rd=self.__no_of_days
        total=self.__basic_cost*self.__no_of_days
        dis=0
        if rd>3:
            dis=total*0.04
        elif rd>1:
            dis=total*0.02
            
        self.__total_amount=total-dis
        return dis