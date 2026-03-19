# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class MeterReading:

    def __init__(self, reading_id:str, meter_code:str, consumer_name:str,
                 consumer_type:str, units_consumed:int, reading_date:date, billing_date:date):
        self.__reading_id = reading_id
        self.__meter_code = meter_code
        self.__consumer_name = consumer_name
        self.__consumer_type = consumer_type
        self.__units_consumed = units_consumed
        self.__reading_date = reading_date
        self.__billing_date = billing_date
        self.__energy_charge = 0.0
        self.__fixed_charge = 0.0
        self.__total_bill = 0.0

    def get_reading_id(self): return self.__reading_id
    def get_meter_code(self): return self.__meter_code
    def get_consumer_name(self): return self.__consumer_name
    def get_consumer_type(self): return self.__consumer_type
    def get_units_consumed(self): return self.__units_consumed
    def get_reading_date(self): return self.__reading_date
    def get_billing_date(self): return self.__billing_date
    def get_energy_charge(self): return self.__energy_charge
    def get_fixed_charge(self): return self.__fixed_charge
    def get_total_bill(self): return self.__total_bill

    def set_reading_id(self, v): self.__reading_id = v
    def set_meter_code(self, v): self.__meter_code = v
    def set_consumer_name(self, v): self.__consumer_name = v
    def set_consumer_type(self, v): self.__consumer_type = v
    def set_units_consumed(self, v): self.__units_consumed = v
    def set_reading_date(self, v): self.__reading_date = v
    def set_billing_date(self, v): self.__billing_date = v
    def set_energy_charge(self, v): self.__energy_charge = v
    def set_fixed_charge(self, v): self.__fixed_charge = v
    def set_total_bill(self, v): self.__total_bill = v

    def calculate_bill(self):
        # Write your code here
        # Business Rules — Unit slab rates by consumer_type:
        #
        # Residential:
        #   units <= 100  -> energy_charge = units * 3.50
        #   units <= 200  -> energy_charge = 100*3.50 + (units-100)*5.00
        #   units > 200   -> energy_charge = 100*3.50 + 100*5.00 + (units-200)*7.50
        #   fixed_charge  = 75.0
        #
        # Commercial:
        #   units <= 300  -> energy_charge = units * 6.00
        #   units > 300   -> energy_charge = 300*6.00 + (units-300)*9.00
        #   fixed_charge  = 200.0
        #
        # Industrial:
        #   units <= 1000 -> energy_charge = units * 5.50
        #   units > 1000  -> energy_charge = 1000*5.50 + (units-1000)*8.00
        #   fixed_charge  = 500.0
        #
        # total_bill = energy_charge + fixed_charge
        # Set all three fields. Return fixed_charge.
        pass
