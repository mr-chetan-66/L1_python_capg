# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date, datetime
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return a list of records (as raw strings) that satisfy:
      1. insurance_status == 'Insured'
      2. (date_of_discharge - date_of_admission).days <= 90
    Each record's fields are comma-separated.
    """
    # Write your code here
    pass


def validate_bill_id(bill_id):
    """
    Validate the bill_id against the business rules:
      - Minimum 4 characters long
      - Must match the pattern: starts with 'BIL' followed by one or more digits
        (regex: ^BIL\d+$)
    Return True if valid, else raise InvalidBillIdException with message 'Invalid Bill Id'.
    """
    # Write your code here
    pass


def validate_ward_type(ward_type):
    """
    Validate that ward_type is one of: 'General', 'Semi-Private', 'Private', 'ICU'
    Return True if valid, else raise InvalidWardTypeException with message 'Invalid Ward Type'.
    """
    # Write your code here
    pass


def convert_date(str_date):
    """
    Convert a date string in 'yyyy-mm-dd' format to a datetime.date object.
    Do NOT use the Pandas package.
    """
    # Write your code here
    pass
