# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class HotelBooking:

    # Parameterized constructor is already defined - do NOT modify it
    def __init__(self, booking_id:str, room_number:str, guest_name:str,
                 room_rate:float, no_of_nights:int, check_in_date:date, room_type:str):
        self.__booking_id = booking_id
        self.__room_number = room_number
        self.__guest_name = guest_name
        self.__room_rate = room_rate
        self.__no_of_nights = no_of_nights
        self.__check_in_date = check_in_date
        self.__room_type = room_type
        self.__base_amount = 0.0
        self.__tax_amount = 0.0
        self.__total_amount = 0.0

    def get_booking_id(self):
        return self.__booking_id

    def get_room_number(self):
        return self.__room_number

    def get_guest_name(self):
        return self.__guest_name

    def get_room_rate(self):
        return self.__room_rate

    def get_no_of_nights(self):
        return self.__no_of_nights

    def get_check_in_date(self):
        return self.__check_in_date

    def get_room_type(self):
        return self.__room_type

    def get_base_amount(self):
        return self.__base_amount

    def get_tax_amount(self):
        return self.__tax_amount

    def get_total_amount(self):
        return self.__total_amount

    def set_booking_id(self, booking_id):
        self.__booking_id = booking_id

    def set_room_number(self, room_number):
        self.__room_number = room_number

    def set_guest_name(self, guest_name):
        self.__guest_name = guest_name

    def set_room_rate(self, room_rate):
        self.__room_rate = room_rate

    def set_no_of_nights(self, no_of_nights):
        self.__no_of_nights = no_of_nights

    def set_check_in_date(self, check_in_date):
        self.__check_in_date = check_in_date

    def set_room_type(self, room_type):
        self.__room_type = room_type

    def set_base_amount(self, base_amount):
        self.__base_amount = base_amount

    def set_tax_amount(self, tax_amount):
        self.__tax_amount = tax_amount

    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount

    def calculate_base_amount(self):
        # Write your code here
        # Business Rule:
        # base_amount = room_rate * no_of_nights
        # Set base_amount and return it
        pass
