# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import date
import exception as ex
import re


def read_file(file):
    """
    Read the given file and return only those records (as raw comma-separated strings) where:
      1. delivery_status == 'Delivered'
      2. (date_of_delivery - date_of_dispatch).days <= 60
    """
    # Write your code here
    pass


def validate_shipment_id(shipment_id):
    """
    Business Rules:
      - Minimum length: 4 characters
      - Must match pattern: starts with 'SHP' followed by one or more digits
        (regex: ^SHP\\d+$)
    Return True if valid.
    Raise InvalidShipmentIdException with message 'Invalid Shipment Id' if invalid.
    """
    # Write your code here
    pass


def validate_zone(zone):
    """
    Valid zones are exactly: 'Zone_A', 'Zone_B', 'Zone_C', 'Zone_D'
    Return True if valid.
    Raise InvalidZoneException with message 'Invalid Zone' if invalid.
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
