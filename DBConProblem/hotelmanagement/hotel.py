### DO NOT ALTER THE GIVEN TEMPLATE.
 
class Hotel:
    def __init__(self,room_no,cust_name,address,phone_number,from_date,to_date):
        self.__room_no = room_no
        self.__cust_name = cust_name
        self.__address = address
        self.__phone_number = phone_number
        self.__from_date = from_date
        self.__to_date = to_date
       
    def get_room_no(self):
        return self.__room_no
    def set_room_no(self,room_no):
        self.__room_no = room_no
       
    def get_cust_name(self):
        return self.__cust_name
    def set_cust_name(self,cust_name):
        self.__cust_name = cust_name
   
    def get_address(self):
        return self.__address
    def set_address(self,address):
        self.address = address
       
    def get_phone_number(self):
        return self.__phone_number
    def set_phone_number(self,phone_number):
        self.__phone_number = phone_number
       
    def get_from_date(self):
        return self.__from_date
    def set_from_date(self,from_date):
        self.__from_date = from_date
       
    def get_to_date(self):
        return self.__to_date
    def set_to_date(self,to_date):
        self.__to_date = to_date