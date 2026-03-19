# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import med_exception as me
import re

def read_file(file):
    # Write your code here
    # Read the file and return only lines where:
    #   1. status (index 8) == 'Verified'
    #   2. expiry_date (index 7) > manufacture_date (index 6)
    #      i.e., the expiry date must be strictly after the manufacture date
    # Return a list of valid line strings.
    pass

def validate_med_code(med_code):
    # Write your code here
    # Business Rule: med_code must be exactly 12 characters.
    #   Pattern: MED-XDDD-RX
    #     - Starts with 'MED-'
    #     - Followed by 1 uppercase letter [A-Z]
    #     - Followed by exactly 3 digits
    #     - Followed by '-RX'
    # If invalid: raise InvalidMedCodeException("Invalid Med Code: <med_code>")
    # If valid: return True
    pass

def validate_stock_id(stock_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters long
    #   - Must match pattern: starts with 'MD' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidStockIdException("Invalid Stock Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert date string DD/MM/YYYY to a Python date object.
    # Do NOT use pandas.
    pass
