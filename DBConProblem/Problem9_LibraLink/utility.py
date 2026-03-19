# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import lib_exception as le
import re

def read_file(file):
    # Write your code here
    # Return only lines where:
    #   1. (return_date - due_date).days <= 30  (return within 30 days of due date)
    # Note: ALL records are included regardless of status — filter only on date gap.
    # Return a list of valid line strings.
    pass

def validate_book_code(book_code):
    # Write your code here
    # Business Rule: book_code must be exactly 11 characters.
    #   Pattern: BK-XXX-DDDD
    #     - Starts with 'BK-'
    #     - Followed by exactly 3 uppercase letters [A-Z]
    #     - Followed by '-'
    #     - Followed by exactly 4 digits
    # If invalid: raise InvalidBookCodeException("Invalid Book Code: <book_code>")
    # If valid: return True
    pass

def validate_issue_id(issue_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters
    #   - Must match: starts with 'LB' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidIssueIdException("Invalid Issue Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Convert DD/MM/YYYY to Python date object. Do NOT use pandas.
    pass
