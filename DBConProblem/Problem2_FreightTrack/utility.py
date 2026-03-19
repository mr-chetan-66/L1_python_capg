# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import freight_exception as fe
import re

def read_file(file):
    # Write your code here
    # Read the file and return only lines where:
    #   1. status (index 7) == 'Dispatched'
    #   2. (dispatch_date - booking_date).days <= 30
    # Return a list of valid line strings.
    pass

def validate_freight_id(freight_id):
    # Write your code here
    # Business Rule: Freight ID must be exactly 10 characters.
    #   - Starts with 'FRT-'
    #   - Followed by exactly 4 digits
    #   - Followed by '-'
    #   - Last 2 characters must be uppercase letters [A-Z]
    # Pattern: FRT-DDDD-AA  (D=digit, A=uppercase letter)
    # If invalid: raise InvalidFreightIdException with message: "Invalid Freight Id: <freight_id>"
    # If valid: return True
    pass

def validate_shipment_id(shipment_id):
    # Write your code here
    # Business Rule: Shipment ID must be at least 5 characters.
    #   - Must start with 'SH' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidShipmentIdException("Invalid Shipment Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert date string DD/MM/YYYY to a Python date object.
    # Do NOT use pandas.
    pass
