### booking.py
### Entity class for Booking

class Booking:
    def __init__(self, booking_id, event_id, customer_name,
                 num_tickets, booking_date, total_amount):
        self.__booking_id    = booking_id
        self.__event_id      = event_id
        self.__customer_name = customer_name
        self.__num_tickets   = num_tickets     # int
        self.__booking_date  = booking_date    # datetime.date object
        self.__total_amount  = total_amount    # float

    def get_booking_id(self):
        return self.__booking_id

    def set_booking_id(self, booking_id):
        self.__booking_id = booking_id

    def get_event_id(self):
        return self.__event_id

    def set_event_id(self, event_id):
        self.__event_id = event_id

    def get_customer_name(self):
        return self.__customer_name

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    def get_num_tickets(self):
        return self.__num_tickets

    def set_num_tickets(self, num_tickets):
        self.__num_tickets = num_tickets

    def get_booking_date(self):
        return self.__booking_date

    def set_booking_date(self, booking_date):
        self.__booking_date = booking_date

    def get_total_amount(self):
        return self.__total_amount

    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount
