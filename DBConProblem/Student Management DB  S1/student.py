### student.py
### Entity class for Student

class Student:
    def __init__(self, student_id, name, department, year, marks):
        self.__student_id = student_id
        self.__name = name
        self.__department = department
        self.__year = year
        self.__marks = marks

    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_year(self):
        return self.__year

    def set_year(self, year):
        self.__year = year

    def get_marks(self):
        return self.__marks

    def set_marks(self, marks):
        self.__marks = marks
