class Flight:
    def __init__(self, flight_id, source, destination, no_of_seats, flight_fare):
        self.__flight_id=flight_id
        self.__source=source
        self.__destination=destination
        self.__no_of_seats=no_of_seats
        self.__flight_fare=flight_fare
       
    def get_flight_id(self):
        return self.__flight_id
       
    def setFlight_id(self,flight_id):
        self.__flight_id = flight_id
       
    def get_source(self):
        return self.__source
       
    def set_source(self,source):
        self.__source = source
   
    def get_destination(self):
        return self.__destination
       
    def set_destination(self,destination):
        self.__destination = destination
       
    def get_no_of_seats(self):
        return self.__no_of_seats
       
    def set_no_of_seats(self,noOfSeats):
        self.__no_of_seats = noOfSeats
       
    def get_flight_fare(self):
        return self.__flight_fare
       
    def set_flight_fare(self,flightFare):
        self.__flight_fare = flightFare


