### employee.py
### Entity class for Employee

class Employee:
    def __init__(self, emp_id, name, designation, department, salary, joining_date):
        self.__emp_id = emp_id
        self.__name = name
        self.__designation = designation
        self.__department = department
        self.__salary = salary
        self.__joining_date = joining_date

    def get_emp_id(self):
        return self.__emp_id

    def set_emp_id(self, emp_id):
        self.__emp_id = emp_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_designation(self):
        return self.__designation

    def set_designation(self, designation):
        self.__designation = designation

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        self.__salary = salary

    def get_joining_date(self):
        return self.__joining_date

    def set_joining_date(self, joining_date):
        self.__joining_date = joining_date
