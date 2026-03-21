from datetime import date

class TravelExpense:

    def __init__(self, expense_id: str, employee_id: str, date_of_travel: date,
                 city_tier: str, date_of_return: date, no_of_days: int,
                 travel_mode: str, approval_status: str):
        self.__expense_id = expense_id
        self.__employee_id = employee_id
        self.__date_of_travel = date_of_travel
        self.__city_tier = city_tier
        self.__date_of_return = date_of_return
        self.__no_of_days = no_of_days
        self.__travel_mode = travel_mode
        self.__approval_status = approval_status
        self.__flight_or_transport_cost = 0.0
        self.__hotel_cost = 0.0
        self.__meal_cost = 0.0
        self.__incidental_allowance = 0.0
        self.__total_expense = 0.0

    def get_expense_id(self):
        return self.__expense_id

    def set_expense_id(self, expense_id):
        self.__expense_id = expense_id

    def get_employee_id(self):
        return self.__employee_id

    def set_employee_id(self, employee_id):
        self.__employee_id = employee_id

    def get_date_of_travel(self):
        return self.__date_of_travel

    def set_date_of_travel(self, date_of_travel):
        self.__date_of_travel = date_of_travel

    def get_city_tier(self):
        return self.__city_tier

    def set_city_tier(self, city_tier):
        self.__city_tier = city_tier

    def get_date_of_return(self):
        return self.__date_of_return

    def set_date_of_return(self, date_of_return):
        self.__date_of_return = date_of_return

    def get_no_of_days(self):
        return self.__no_of_days

    def set_no_of_days(self, no_of_days):
        self.__no_of_days = no_of_days

    def get_travel_mode(self):
        return self.__travel_mode

    def set_travel_mode(self, travel_mode):
        self.__travel_mode = travel_mode

    def get_approval_status(self):
        return self.__approval_status

    def set_approval_status(self, approval_status):
        self.__approval_status = approval_status

    def get_flight_or_transport_cost(self):
        return self.__flight_or_transport_cost

    def set_flight_or_transport_cost(self, flight_or_transport_cost):
        self.__flight_or_transport_cost = flight_or_transport_cost

    def get_hotel_cost(self):
        return self.__hotel_cost

    def set_hotel_cost(self, hotel_cost):
        self.__hotel_cost = hotel_cost

    def get_meal_cost(self):
        return self.__meal_cost

    def set_meal_cost(self, meal_cost):
        self.__meal_cost = meal_cost

    def get_incidental_allowance(self):
        return self.__incidental_allowance

    def set_incidental_allowance(self, incidental_allowance):
        self.__incidental_allowance = incidental_allowance

    def get_total_expense(self):
        return self.__total_expense

    def set_total_expense(self, total_expense):
        self.__total_expense = total_expense
