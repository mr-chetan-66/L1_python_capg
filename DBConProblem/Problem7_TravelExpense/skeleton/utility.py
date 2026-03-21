# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated
    strings) where ALL of the following are true:
      1. approval_status == 'Approved'
      2. (date_of_return - date_of_travel).days <= 45
    """
    # Write your code here
    pass


def validate_expense_id(expense_id):
    """
    Business Rules:
      - Minimum length: 5 characters
      - Must match pattern: starts with 'EXP' followed by one or more digits
        (regex: ^EXP\\d+$)
    Return True if valid.
    Raise InvalidExpenseIdException with message 'Invalid Expense Id' if invalid.
    """
    # Write your code here
    pass


def validate_city_tier(city_tier):
    """
    Valid city tiers are exactly: 'Tier1', 'Tier2', 'Tier3'
    Return True if valid.
    Raise InvalidCityTierException with message 'Invalid City Tier' if invalid.
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
