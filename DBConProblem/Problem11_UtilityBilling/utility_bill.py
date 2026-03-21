# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class UtilityBill:

    def __init__(self,bill_id:str,consumer_id:str,billing_date:date,consumer_type:str,reading_date:date,units_consumed:float,connection_type:str,payment_status:str):
        self.__bill_id=bill_id
        self.__consumer_id=consumer_id
        self.__billing_date=billing_date
        self.__consumer_type=consumer_type
        self.__reading_date=reading_date
        self.__units_consumed=units_consumed
        self.__connection_type=connection_type
        self.__payment_status=payment_status
        self.__energy_charge=0.0
        self.__fixed_charge=0.0
        self.__tax=0.0
        self.__total_bill_amount=0.0

    def get_bill_id(self):
        return self.__bill_id
    def set_bill_id(self, bill_id):
        self.__bill_id = bill_id

    def get_consumer_id(self):
        return self.__consumer_id
    def set_consumer_id(self, consumer_id):
        self.__consumer_id = consumer_id

    def get_billing_date(self):
        return self.__billing_date
    def set_billing_date(self, billing_date):
        self.__billing_date = billing_date

    def get_consumer_type(self):
        return self.__consumer_type
    def set_consumer_type(self, consumer_type):
        self.__consumer_type = consumer_type

    def get_reading_date(self):
        return self.__reading_date
    def set_reading_date(self, reading_date):
        self.__reading_date = reading_date

    def get_units_consumed(self):
        return self.__units_consumed
    def set_units_consumed(self, units_consumed):
        self.__units_consumed = units_consumed

    def get_connection_type(self):
        return self.__connection_type
    def set_connection_type(self, connection_type):
        self.__connection_type = connection_type

    def get_payment_status(self):
        return self.__payment_status
    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status

    def get_energy_charge(self):
        return self.__energy_charge
    def set_energy_charge(self, energy_charge):
        self.__energy_charge = energy_charge

    def get_fixed_charge(self):
        return self.__fixed_charge
    def set_fixed_charge(self, fixed_charge):
        self.__fixed_charge = fixed_charge

    def get_tax(self):
        return self.__tax
    def set_tax(self, tax):
        self.__tax = tax

    def get_total_bill_amount(self):
        return self.__total_bill_amount
    def set_total_bill_amount(self, total_bill_amount):
        self.__total_bill_amount = total_bill_amount
