from datetime import date

class UtilityBill:

    def __init__(self, bill_id: str, consumer_id: str, billing_date: date,
                 consumer_type: str, reading_date: date,
                 units_consumed: float, connection_type: str,
                 payment_status: str):
        self.__bill_id = bill_id
        self.__consumer_id = consumer_id
        self.__billing_date = billing_date
        self.__consumer_type = consumer_type
        self.__reading_date = reading_date
        self.__units_consumed = units_consumed
        self.__connection_type = connection_type
        self.__payment_status = payment_status
        self.__energy_charge = 0.0
        self.__fixed_charge = 0.0
        self.__tax = 0.0
        self.__total_bill_amount = 0.0

    def get_bill_id(self): return self.__bill_id
    def set_bill_id(self, v): self.__bill_id = v

    def get_consumer_id(self): return self.__consumer_id
    def set_consumer_id(self, v): self.__consumer_id = v

    def get_billing_date(self): return self.__billing_date
    def set_billing_date(self, v): self.__billing_date = v

    def get_consumer_type(self): return self.__consumer_type
    def set_consumer_type(self, v): self.__consumer_type = v

    def get_reading_date(self): return self.__reading_date
    def set_reading_date(self, v): self.__reading_date = v

    def get_units_consumed(self): return self.__units_consumed
    def set_units_consumed(self, v): self.__units_consumed = v

    def get_connection_type(self): return self.__connection_type
    def set_connection_type(self, v): self.__connection_type = v

    def get_payment_status(self): return self.__payment_status
    def set_payment_status(self, v): self.__payment_status = v

    def get_energy_charge(self): return self.__energy_charge
    def set_energy_charge(self, v): self.__energy_charge = v

    def get_fixed_charge(self): return self.__fixed_charge
    def set_fixed_charge(self, v): self.__fixed_charge = v

    def get_tax(self): return self.__tax
    def set_tax(self, v): self.__tax = v

    def get_total_bill_amount(self): return self.__total_bill_amount
    def set_total_bill_amount(self, v): self.__total_bill_amount = v
