### event.py
### Entity class for Event

class Event:
    def __init__(self, event_id, event_name, venue, event_date,
                 event_time, total_seats, booked_seats, ticket_price):
        self.__event_id      = event_id
        self.__event_name    = event_name
        self.__venue         = venue
        self.__event_date    = event_date      # datetime.date object
        self.__event_time    = event_time      # datetime.time object
        self.__total_seats   = total_seats     # int
        self.__booked_seats  = booked_seats    # int
        self.__ticket_price  = ticket_price    # float

    def get_event_id(self):
        return self.__event_id

    def set_event_id(self, event_id):
        self.__event_id = event_id

    def get_event_name(self):
        return self.__event_name

    def set_event_name(self, event_name):
        self.__event_name = event_name

    def get_venue(self):
        return self.__venue

    def set_venue(self, venue):
        self.__venue = venue

    def get_event_date(self):
        return self.__event_date

    def set_event_date(self, event_date):
        self.__event_date = event_date

    def get_event_time(self):
        return self.__event_time

    def set_event_time(self, event_time):
        self.__event_time = event_time

    def get_total_seats(self):
        return self.__total_seats

    def set_total_seats(self, total_seats):
        self.__total_seats = total_seats

    def get_booked_seats(self):
        return self.__booked_seats

    def set_booked_seats(self, booked_seats):
        self.__booked_seats = booked_seats

    def get_ticket_price(self):
        return self.__ticket_price

    def set_ticket_price(self, ticket_price):
        self.__ticket_price = ticket_price
