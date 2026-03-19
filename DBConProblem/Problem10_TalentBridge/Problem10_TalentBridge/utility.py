# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import talent_exception as te
import re

def read_file(file):
    # Write your code here
    # Return only lines where:
    #   1. status (index 8) == 'Shortlisted'
    #   2. (application_date - closing_date).days <= 15
    # Return a list of valid line strings.
    pass

def validate_job_code(job_code):
    # Write your code here
    # Business Rule: job_code must be exactly 11 characters.
    #   Pattern: JOB-XX-DDDD
    #     - Starts with 'JOB-'
    #     - Followed by exactly 2 uppercase letters [A-Z]
    #     - Followed by '-'
    #     - Followed by exactly 4 digits
    # If invalid: raise InvalidJobCodeException("Invalid Job Code: <job_code>")
    # If valid: return True
    pass

def validate_application_id(application_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match: starts with 'JA' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidApplicationIdException("Invalid Application Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Convert DD/MM/YYYY to Python date object. Do NOT use pandas.
    pass
