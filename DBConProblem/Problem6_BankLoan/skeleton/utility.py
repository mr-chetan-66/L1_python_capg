# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated strings) where:
      1. loan_status == 'Approved'
      2. (date_of_disbursement - date_of_application).days <= 30
         i.e. the loan was disbursed within 30 days of application
    """
    # Write your code here
    pass


def validate_loan_id(loan_id):
    """
    Business Rules:
      - Minimum length: 5 characters
      - Must match pattern: starts with 'LN' followed by one or more digits
        (regex: ^LN\\d+$)
    Return True if valid.
    Raise InvalidLoanIdException with message 'Invalid Loan Id' if invalid.
    """
    # Write your code here
    pass


def validate_loan_type(loan_type):
    """
    Valid loan types are exactly:
      'Home', 'Vehicle', 'Personal', 'Education'
    Return True if valid.
    Raise InvalidLoanTypeException with message 'Invalid Loan Type' if invalid.
    """
    # Write your code here
    pass


def convert_date(str_date):
    """
    Convert a date string 'yyyy-mm-dd' to a datetime.date object.
    Do NOT use Pandas.
    """
    # Write your code here
    pass
