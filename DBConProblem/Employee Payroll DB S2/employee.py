### employee.py
### Entity class for Employee

class Employee:
    def __init__(self, emp_id, emp_name, department, designation,
                 basic_salary, joining_date):
        self.__emp_id        = emp_id
        self.__emp_name      = emp_name
        self.__department    = department
        self.__designation   = designation
        self.__basic_salary  = basic_salary    # float
        self.__joining_date  = joining_date    # datetime.date object

    def get_emp_id(self):
        return self.__emp_id

    def set_emp_id(self, emp_id):
        self.__emp_id = emp_id

    def get_emp_name(self):
        return self.__emp_name

    def set_emp_name(self, emp_name):
        self.__emp_name = emp_name

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_designation(self):
        return self.__designation

    def set_designation(self, designation):
        self.__designation = designation

    def get_basic_salary(self):
        return self.__basic_salary

    def set_basic_salary(self, basic_salary):
        self.__basic_salary = basic_salary

    def get_joining_date(self):
        return self.__joining_date

    def set_joining_date(self, joining_date):
        self.__joining_date = joining_date
