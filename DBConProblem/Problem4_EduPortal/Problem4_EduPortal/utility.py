# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import edu_exception as ee
import re

def read_file(file):
    # Write your code here
    # Read the file and return only lines where:
    #   1. status (index 8) == 'Active'
    #   2. (start_date - registration_date).days <= 20
    # Return a list of valid line strings.
    pass

def validate_course_code(course_code):
    # Write your code here
    # Business Rule: course_code must be exactly 11 characters.
    #   Pattern: CRS-XX-DDDD
    #     - Starts with 'CRS-'
    #     - Followed by exactly 2 uppercase letters [A-Z]
    #     - Followed by '-'
    #     - Followed by exactly 4 digits
    # If invalid: raise InvalidCourseCodeException("Invalid Course Code: <course_code>")
    # If valid: return True
    pass

def validate_enrollment_id(enrollment_id):
    # Write your code here
    # Business Rule:
    #   - Must be at least 5 characters long
    #   - Must match pattern: starts with 'EN' followed by 3 or more digits
    # If length < 5 OR pattern mismatch: raise InvalidEnrollmentIdException("Invalid Enrollment Id")
    # If valid: return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert date string DD/MM/YYYY to a Python date object.
    # Do NOT use pandas.
    pass
