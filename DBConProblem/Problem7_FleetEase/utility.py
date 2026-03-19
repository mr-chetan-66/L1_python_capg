# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import fleet_exception as fe
import re

def read_file(file):
    # Write your code here
    # Return only lines where:
    #   1. status (index 7) == 'Approved'
    #   2. (service_date - booking_date).days <= 10
    # Return a list of valid line strings.
    pass

def validate_vehicle_id(vehicle_id):
    # Write your code here
    # Business Rule: vehicle_id must be exactly 11 characters.
    #   Pattern: VEH-XXX-DDD
    #     - Starts with 'VEH-'
    #     - Followed by exactly 3 uppercase letters [A-Z]
    #     - Followed by '-'
    #     - Followed by exactly 3 digits
    # If invalid: raise InvalidVehicleIdException("Invalid Vehicle Id: <vehicle_id>")
    # If valid: return True
    pass

def validate_service_id(service_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match: starts with 'VS' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidServiceIdException("Invalid Service Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Convert DD/MM/YYYY to Python date object. Do NOT use pandas.
    pass
