# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated
    strings) where ALL THREE of the following are true:
      1. payment_status == 'Pending'
      2. units_consumed >= 50
      3. (reading_date - billing_date).days <= 60
    """
    # Write your code here
    pass


def validate_bill_id(bill_id):
    """
    Business Rules:
      - Minimum length: 6 characters
      - Must match pattern: starts with 'ENB' followed by one or more digits
        (regex: ^ENB\\d+$)
    Return True if valid.
    Raise InvalidBillIdException with message 'Invalid Bill Id' if invalid.
    """
    # Write your code here
    pass


def validate_consumer_type(consumer_type):
    """
    Valid consumer types: 'Residential', 'Commercial', 'Industrial', 'Agricultural'
    Return True if valid.
    Raise InvalidConsumerTypeException with message 'Invalid Consumer Type' if invalid.
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
