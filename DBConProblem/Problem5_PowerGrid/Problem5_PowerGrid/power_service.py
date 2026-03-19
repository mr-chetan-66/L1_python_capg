# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import meter_reading as mr
from datetime import timedelta
import oracledb
import power_exception as pe

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class PowerService:

    def __init__(self):
        self.__fixed_charge_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line in records:
        #   1. Validate meter_code — catch InvalidMeterCodeException and print message
        #   2. Validate reading_id — catch InvalidReadingIdException and print message
        #   3. Convert reading_date and billing_date using utility
        #   4. Create MeterReading object
        #   5. Call calculate_bill() — store fixed_charge in self.__fixed_charge_dict keyed by reading_id
        #   6. Call add_reading_details() to insert into DB
        # Truncate the MeterReading table at the start.
        # Return None.
        pass

    def add_reading_details(self, obj):
        # Write your code here
        # Insert the MeterReading object into the 'MeterReading' table.
        # Column order: reading_id, meter_code, consumer_name, consumer_type,
        #               units_consumed, reading_date, billing_date,
        #               energy_charge, fixed_charge, total_bill
        # Return None.
        pass

    def find_top3_meters(self):
        # Write your code here
        # Count how many times each meter_code appears in MeterReading table.
        # Return {meter_code: count} of top 3 distinct counts, sorted descending.
        # Handle ties — all meter_codes within top 3 distinct values must be included.
        pass

    def search_reading(self, reading_id):
        # Write your code here
        # Query MeterReading table for given reading_id.
        # Return fully populated MeterReading object, or None if not found.
        pass

    def find_high_consumption(self, start_date, end_date):
        # Write your code here
        # Find all readings where:
        #   - units_consumed > 300
        #   - reading_date is between start_date and end_date (inclusive)
        # Return {reading_id: units_consumed}. Return empty dict if none found.
        pass

    def update_fixed_charge(self, consumer_type):
        # Write your code here
        # For all readings matching the given consumer_type:
        #   UPDATE: fixed_charge = fixed_charge * 1.10
        #           total_bill = energy_charge + (fixed_charge * 1.10)
        # After update, SELECT all readings with that consumer_type.
        # Return list of MeterReading objects with updated values, or None if none found.
        pass
