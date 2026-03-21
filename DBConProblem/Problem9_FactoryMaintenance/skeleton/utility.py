# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated
    strings) where ALL THREE of the following are true:
      1. maintenance_status == 'Scheduled'
      2. operating_hours >= 100
      3. (date_of_next_service - date_of_last_service).days <= 365
    """
    # Write your code here
    pass


def validate_maintenance_id(maintenance_id):
    """
    Business Rules:
      - Minimum length: 6 characters
      - Must match pattern: starts with 'MNT' followed by one or more digits
        (regex: ^MNT\\d+$)
    Return True if valid.
    Raise InvalidMaintenanceIdException with message 'Invalid Maintenance Id' if invalid.
    """
    # Write your code here
    pass


def validate_equipment_type(equipment_type):
    """
    Valid types: 'CNC', 'Hydraulic', 'Conveyor', 'Electrical'
    Return True if valid.
    Raise InvalidEquipmentTypeException with message 'Invalid Equipment Type' if invalid.
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
