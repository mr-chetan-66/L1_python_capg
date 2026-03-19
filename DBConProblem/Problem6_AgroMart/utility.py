# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import agro_exception as ae
import re

def read_file(file):
    # Write your code here
    # Return only lines where:
    #   1. status (index 9) == 'Ready'
    #   2. (harvest_date - listing_date).days <= 20
    # Return a list of valid line strings.
    pass

def validate_crop_code(crop_code):
    # Write your code here
    # Business Rule: crop_code must be exactly 11 characters.
    #   Pattern: CRP-XDD-DDD
    #     - Starts with 'CRP-'
    #     - Followed by 1 uppercase letter [A-Z]
    #     - Followed by exactly 2 digits
    #     - Followed by '-'
    #     - Followed by exactly 3 digits
    # If invalid: raise InvalidCropCodeException("Invalid Crop Code: <crop_code>")
    # If valid: return True
    pass

def validate_agri_id(agri_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match: starts with 'AG' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidAgriIdException("Invalid Agri Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert DD/MM/YYYY string to Python date object. Do NOT use pandas.
    pass
