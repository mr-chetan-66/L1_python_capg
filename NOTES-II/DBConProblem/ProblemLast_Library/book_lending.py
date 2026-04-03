# DO NOT CHANGE THIS FILE
from datetime import date

class BookLending:

    def __init__(self, lending_id: str, student_id: str, date_of_lending: date,
                 membership_type: str, due_date: date, no_of_books: int,
                 late_days: int, payment_status: str):

        self.__lending_id = lending_id
        self.__student_id = student_id
        self.__date_of_lending = date_of_lending
        self.__membership_type = membership_type
        self.__due_date = due_date
        self.__no_of_books = no_of_books
        self.__late_days = late_days
        self.__payment_status = payment_status
        self.__base_charge = 0.0
        self.__late_fine = 0.0
        self.__discount = 0.0
        self.__net_amount = 0.0

    def get_lending_id(self):
        return self.__lending_id

    def set_lending_id(self, lending_id):
        self.__lending_id = lending_id

    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def get_date_of_lending(self):
        return self.__date_of_lending

    def set_date_of_lending(self, date_of_lending):
        self.__date_of_lending = date_of_lending

    def get_membership_type(self):
        return self.__membership_type

    def set_membership_type(self, membership_type):
        self.__membership_type = membership_type

    def get_due_date(self):
        return self.__due_date

    def set_due_date(self, due_date):
        self.__due_date = due_date

    def get_no_of_books(self):
        return self.__no_of_books

    def set_no_of_books(self, no_of_books):
        self.__no_of_books = no_of_books

    def get_late_days(self):
        return self.__late_days

    def set_late_days(self, late_days):
        self.__late_days = late_days

    def get_payment_status(self):
        return self.__payment_status

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status

    def get_base_charge(self):
        return self.__base_charge

    def set_base_charge(self, base_charge):
        self.__base_charge = base_charge

    def get_late_fine(self):
        return self.__late_fine

    def set_late_fine(self, late_fine):
        self.__late_fine = late_fine

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    def get_net_amount(self):
        return self.__net_amount

    def set_net_amount(self, net_amount):
        self.__net_amount = net_amount
