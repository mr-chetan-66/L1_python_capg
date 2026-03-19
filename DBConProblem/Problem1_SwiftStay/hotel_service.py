# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import hotel_booking as hb
from datetime import timedelta
import oracledb
import hotel_exception as he

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class HotelService:

    def __init__(self):
        self.__tax_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line in records:
        #   1. Validate room_number using utility - catch InvalidRoomNumberException and print message
        #   2. Validate booking_id using utility - catch InvalidBookingIdException and print message
        #   3. Convert check_in_date using utility
        #   4. Create HotelBooking object
        #   5. Call calculate_base_amount() on the object
        #   6. Call calculate_tax() to get tax and total, set them on the object
        #   7. Call add_booking_details() to insert into DB
        #   8. Store tax in self.__tax_dict with booking_id as key
        # Truncate the HotelBooking table at the start before inserting
        # This method should return None
        pass

    def calculate_tax(self, room_type, base_amount):
        # Write your code here
        # Tax rates by room type:
        #   Suite    -> 18%
        #   Deluxe   -> 12%
        #   Standard -> 8%
        # tax_amount = base_amount * tax_rate
        # total_amount = base_amount + tax_amount
        # Return (tax_amount, total_amount) as a tuple
        pass

    def add_booking_details(self, obj):
        # Write your code here
        # Insert the HotelBooking object into the 'HotelBooking' table
        # Column order: booking_id, room_number, guest_name, room_rate, no_of_nights,
        #               check_in_date, room_type, base_amount, tax_amount, total_amount
        # This method should return None
        pass

    def find_top3_rooms(self):
        # Write your code here
        # Count how many times each room_number appears in the HotelBooking table
        # Identify the top 3 distinct rental counts
        # Return a dictionary {room_number: count} sorted by count in descending order
        # Include ALL rooms whose count falls within the top 3 distinct count values
        # (i.e., ties at a given rank level are all included)
        pass

    def search_booking(self, booking_id):
        # Write your code here
        # Query the HotelBooking table for the given booking_id
        # If found, build and return a HotelBooking object with all fields populated
        # If not found, return None
        pass

    def find_checkout_dates(self, start_date, end_date):
        # Write your code here
        # Find all bookings where:
        #   - no_of_nights > 5
        #   - check_in_date is between start_date and end_date (inclusive)
        # Checkout date = check_in_date + no_of_nights (timedelta)
        # Return a dictionary {booking_id: checkout_date}
        # Return empty dict if no records found
        pass

    def update_tax_rates(self, room_type):
        # Write your code here
        # For all bookings matching the given room_type:
        #   UPDATE: tax_amount = tax_amount * 1.1
        #           total_amount = base_amount + (tax_amount * 1.1)
        # After update, SELECT all bookings with the given room_type
        # Build and return a list of HotelBooking objects with updated values
        # Return None if no records are found
        pass
