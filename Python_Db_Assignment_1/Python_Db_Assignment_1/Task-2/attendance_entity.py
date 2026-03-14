class Attendance:
    
    # Define the parameterized constructor here
    def __init__(self, employee_id, date, status):
        self.__employee_id = employee_id
        self.__date = date
        self.__status = status

    # Setters (optional)
    def set_employee_id(self, value): self.__employee_id = value
    def set_date(self, value): self.__date = value
    def set_status(self, value): self.__status = value

    # Getters
    def get_employee_id(self): return self.__employee_id
    def get_date(self): return self.__date
    def get_status(self): return self.__status

    def __repr__(self):
        return f"Attendance(employee_id={self.__employee_id}, date='{self.__date}', status='{self.__status}')"