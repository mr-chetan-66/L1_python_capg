# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class ScholarshipApplication:

    def __init__(self,application_id:str,student_id:str,date_of_application:date,course_type:str,date_of_enrollment:date,cgpa:float,annual_family_income:float,category:str,application_status:str):
        self.__application_id = application_id
        self.__student_id = student_id
        self.__date_of_application = date_of_application
        self.__course_type = course_type
        self.__date_of_enrollment = date_of_enrollment
        self.__cgpa = cgpa
        self.__annual_family_income = annual_family_income
        self.__category = category
        self.__application_status = application_status
        self.__base_scholarship = 0.0
        self.__merit_bonus = 0.0
        self.__income_waiver = 0.0
        self.__total_scholarship = 0.0
    # Write all getters and setters for the private attributes below

    def get_application_id(self):
        return self.__application_id

    def set_application_id(self, application_id):
        self.__application_id = application_id

    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def get_date_of_application(self):
        return self.__date_of_application

    def set_date_of_application(self, date_of_application):
        self.__date_of_application = date_of_application

    def get_course_type(self):
        return self.__course_type

    def set_course_type(self, course_type):
        self.__course_type = course_type

    def get_date_of_enrollment(self):
        return self.__date_of_enrollment

    def set_date_of_enrollment(self, date_of_enrollment):
        self.__date_of_enrollment = date_of_enrollment

    def get_cgpa(self):
        return self.__cgpa

    def set_cgpa(self, cgpa):
        self.__cgpa = cgpa

    def get_annual_family_income(self):
        return self.__annual_family_income

    def set_annual_family_income(self, annual_family_income):
        self.__annual_family_income = annual_family_income

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_application_status(self):
        return self.__application_status

    def set_application_status(self, application_status):
        self.__application_status = application_status

    def get_base_scholarship(self):
        return self.__base_scholarship

    def set_base_scholarship(self, base_scholarship):
        self.__base_scholarship = base_scholarship

    def get_merit_bonus(self):
        return self.__merit_bonus

    def set_merit_bonus(self, merit_bonus):
        self.__merit_bonus = merit_bonus

    def get_income_waiver(self):
        return self.__income_waiver

    def set_income_waiver(self, income_waiver):
        self.__income_waiver = income_waiver

    def get_total_scholarship(self):
        return self.__total_scholarship

    def set_total_scholarship(self, total_scholarship):
        self.__total_scholarship = total_scholarship
