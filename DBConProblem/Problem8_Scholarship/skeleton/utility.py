# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated
    strings) where ALL of the following conditions are true:
      1. application_status == 'Eligible'
      2. cgpa >= 6.0
      3. (date_of_application - date_of_enrollment).days <= 120
         i.e. the student applied within 120 days of enrolling
    """
    # Write your code here
    pass


def validate_application_id(application_id):
    """
    Business Rules:
      - Minimum length: 6 characters
      - Must match pattern: starts with 'SCH' followed by one or more digits
        (regex: ^SCH\\d+$)
    Return True if valid.
    Raise InvalidApplicationIdException with message 'Invalid Application Id'
    if invalid.
    """
    # Write your code here
    pass


def validate_course_type(course_type):
    """
    Valid course types are exactly:
      'UG', 'PG', 'Diploma', 'PhD'
    Return True if valid.
    Raise InvalidCourseTypeException with message 'Invalid Course Type' if invalid.
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
