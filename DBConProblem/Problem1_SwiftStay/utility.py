# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import hotel_exception as he
import re

def read_file(file):
    # Write your code here
    # Read the file and return only lines where:
    #   1. status (index 7) == 'Confirmed'
    #   2. (check_in_date - booking_date).days <= 60
    # Return a list of valid line strings
    pass

def validate_room_number(room_number):
    # Write your code here
    # Business Rule: Room number must be exactly 10 characters
    #   - Starts with 'RMH'
    #   - Followed by exactly 3 digits
    #   - Followed by any 3 characters
    #   - Last character must be an uppercase letter [A-Z]
    # If invalid, raise InvalidRoomNumberException with message: "Invalid Room Number: <room_number>"
    # If valid, return True
    pass

def validate_booking_id(booking_id):
    # Write your code here
    # Business Rule: Booking ID must be at least 5 characters long
    #   - Must match pattern: starts with 'BK' followed by 3 or more digits
    # If invalid (length < 5 OR pattern mismatch), raise InvalidBookingIdException
    #   with message: "Invalid Booking Id"
    # If valid, return True
    pass

def convert_date(str_date):
    # Write your code here
    # Convert date string in format DD/MM/YYYY to a Python date object
    # Note: Do NOT use the pandas package
    pass
