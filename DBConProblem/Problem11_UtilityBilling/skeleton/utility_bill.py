# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class UtilityBill:

    # Define the parameterized constructor here
    # Parameters: bill_id, consumer_id, billing_date, consumer_type,
    #             reading_date, units_consumed, connection_type, payment_status
    # Default values: energy_charge=0.0, fixed_charge=0.0,
    #                 tax=0.0, total_bill_amount=0.0
    def __init__(self, bill_id: str, consumer_id: str, billing_date: date,
                 consumer_type: str, reading_date: date,
                 units_consumed: float, connection_type: str,
                 payment_status: str):
        # Write your code here
        pass

    # Write all getters and setters for the private attributes below

    def get_bill_id(self):
        pass
    def set_bill_id(self, bill_id):
        pass

    def get_consumer_id(self):
        pass
    def set_consumer_id(self, consumer_id):
        pass

    def get_billing_date(self):
        pass
    def set_billing_date(self, billing_date):
        pass

    def get_consumer_type(self):
        pass
    def set_consumer_type(self, consumer_type):
        pass

    def get_reading_date(self):
        pass
    def set_reading_date(self, reading_date):
        pass

    def get_units_consumed(self):
        pass
    def set_units_consumed(self, units_consumed):
        pass

    def get_connection_type(self):
        pass
    def set_connection_type(self, connection_type):
        pass

    def get_payment_status(self):
        pass
    def set_payment_status(self, payment_status):
        pass

    def get_energy_charge(self):
        pass
    def set_energy_charge(self, energy_charge):
        pass

    def get_fixed_charge(self):
        pass
    def set_fixed_charge(self, fixed_charge):
        pass

    def get_tax(self):
        pass
    def set_tax(self, tax):
        pass

    def get_total_bill_amount(self):
        pass
    def set_total_bill_amount(self, total_bill_amount):
        pass
