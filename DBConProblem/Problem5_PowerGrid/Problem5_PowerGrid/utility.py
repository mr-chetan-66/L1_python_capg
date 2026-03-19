# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import power_exception as pe
import re

def read_file(file):
    # Write your code here
    # Read the file and return only lines where:
    #   1. status (index 7) == 'Active'
    #   2. (reading_date - billing_date).days <= 15
    # Return a list of valid line strings.
    pass

def validate_meter_code(meter_code):
    # Write your code here
    # Business Rule: meter_code must be exactly 12 characters.
    #   Pattern: MTR-XDD-DDDD
    #     - Starts with 'MTR-'
    #     - Followed by 1 uppercase letter [A-Z]
    #     - Followed by exactly 2 digits
    #     - Followed by '-'
    #     - Followed by exactly 4 digits
    # If invalid: raise InvalidMeterCodeException("Invalid Meter Code: <meter_code>")
    # If valid: return True
    pass

def validate_reading_id(reading_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match pattern: starts with 'MR' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidReadingIdException("Invalid Reading Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert date string DD/MM/YYYY to a Python date object.
    # Do NOT use pandas.
    pass
