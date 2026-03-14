# empreimbursement.py
from datetime import date

class EmpReimbursement:

    def __init__(self, request_id: str, employee_code: str, date_of_request: date,
                 grade: str, date_of_travel: date, no_of_days_of_stay: int,
                 local_travel_in_kms: float, manager_approval: str):
        # Private attributes
        self.__request_id = request_id
        self.__employee_code = employee_code
        self.__date_of_request = date_of_request
        self.__grade = grade
        self.__date_of_travel = date_of_travel
        self.__no_of_days_of_stay = no_of_days_of_stay
        self.__local_travel_in_kms = local_travel_in_kms
        self.__manager_approval = manager_approval
        # Defaults
        self.__accomodation_cost = 0.0
        self.__dining_cost = 0.0
        self.__allowances = 0.0
        self.__local_travel_cost = 0.0
        self.__total_reimbursement_cost = 0.0

    # -------- Getters --------
    def get_request_id(self): return self.__request_id
    def get_employee_code(self): return self.__employee_code
    def get_date_of_request(self): return self.__date_of_request
    def get_grade(self): return self.__grade
    def get_date_of_travel(self): return self.__date_of_travel
    def get_no_of_days_of_stay(self): return self.__no_of_days_of_stay
    def get_local_travel_in_kms(self): return self.__local_travel_in_kms
    def get_manager_approval(self): return self.__manager_approval
    def get_accomodation_cost(self): return self.__accomodation_cost
    def get_dining_cost(self): return self.__dining_cost
    def get_allowances(self): return self.__allowances
    def get_local_travel_cost(self): return self.__local_travel_cost
    def get_total_reimbursement_cost(self): return self.__total_reimbursement_cost

    # -------- Setters --------
    def set_request_id(self, v: str): self.__request_id = v
    def set_employee_code(self, v: str): self.__employee_code = v
    def set_date_of_request(self, v: date): self.__date_of_request = v
    def set_grade(self, v: str): self.__grade = v
    def set_date_of_travel(self, v: date): self.__date_of_travel = v
    def set_no_of_days_of_stay(self, v: int): self.__no_of_days_of_stay = v
    def set_local_travel_in_kms(self, v: float): self.__local_travel_in_kms = v
    def set_manager_approval(self, v: str): self.__manager_approval = v
    def set_accomodation_cost(self, v: float): self.__accomodation_cost = v
    def set_dining_cost(self, v: float): self.__dining_cost = v
    def set_allowances(self, v: float): self.__allowances = v
    def set_local_travel_cost(self, v: float): self.__local_travel_cost = v
    def set_total_reimbursement_cost(self, v: float): self.__total_reimbursement_cost = v

    # Convenience for printing in sample format
    def to_display_lines(self):
        # Sample output shows time part ("00:00:00") and days as floating like "9.0"
        date_travel_out = f"{self.__date_of_travel} 00:00:00"
        days_out = f"{float(self.__no_of_days_of_stay):.1f}"
        return [
            f"Request Id: {self.__request_id}",
            f"Employee Code: {self.__employee_code}",
            f"Date of Travel: {date_travel_out}",
            f"No.of Days: {days_out}",
            f"Accommodation Cost: {self.__accomodation_cost:.1f}",
            f"Dinning Cost: {self.__dining_cost:.1f}",
            f"Local Travel cost: {self.__local_travel_cost:.1f}",
            f"Allowances: {self.__allowances:.1f}",
            f"Total Reimbursement Amount: {self.__total_reimbursement_cost:.1f}",
        ]