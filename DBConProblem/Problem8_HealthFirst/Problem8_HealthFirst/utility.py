# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import health_exception as he
import re

def read_file(file):
    # Write your code here
    # Return only lines where:
    #   1. status (index 7) == 'Approved'
    #   2. (claim_date - policy_date).days <= 45
    # Return a list of valid line strings.
    pass

def validate_policy_id(policy_id):
    # Write your code here
    # Business Rule: policy_id must be exactly 11 characters.
    #   Pattern: POL-XDD-DDD
    #     - Starts with 'POL-'
    #     - Followed by 1 uppercase letter [A-Z]
    #     - Followed by exactly 2 digits
    #     - Followed by '-'
    #     - Followed by exactly 3 digits
    # If invalid: raise InvalidPolicyIdException("Invalid Policy Id: <policy_id>")
    # If valid: return True
    pass

def validate_claim_id(claim_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match: starts with 'CL' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidClaimIdException("Invalid Claim Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Convert DD/MM/YYYY to Python date object. Do NOT use pandas.
    pass
