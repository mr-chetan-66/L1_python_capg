# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class JobApplication:

    def get_application_id(self): return self.__application_id
    def get_job_code(self): return self.__job_code
    def get_applicant_name(self): return self.__applicant_name
    def get_experience_grade(self): return self.__experience_grade
    def get_years_exp(self): return self.__years_exp
    def get_application_date(self): return self.__application_date
    def get_closing_date(self): return self.__closing_date
    def get_job_title(self): return self.__job_title
    def get_base_salary(self): return self.__base_salary
    def get_experience_bonus(self): return self.__experience_bonus
    def get_offered_salary(self): return self.__offered_salary

    def set_application_id(self, v): self.__application_id = v
    def set_job_code(self, v): self.__job_code = v
    def set_applicant_name(self, v): self.__applicant_name = v
    def set_experience_grade(self, v): self.__experience_grade = v
    def set_years_exp(self, v): self.__years_exp = v
    def set_application_date(self, v): self.__application_date = v
    def set_closing_date(self, v): self.__closing_date = v
    def set_job_title(self, v): self.__job_title = v
    def set_base_salary(self, v): self.__base_salary = v
    def set_experience_bonus(self, v): self.__experience_bonus = v
    def set_offered_salary(self, v): self.__offered_salary = v

    def calculate_offered_salary(self):
        # Write your code here
        # Business Rule — Base salary and bonus rate by experience_grade:
        #   Junior -> base_salary = 25000.0, bonus_rate = 0.30
        #   Mid    -> base_salary = 40000.0, bonus_rate = 0.50
        #   Senior -> base_salary = 60000.0, bonus_rate = 0.70
        #   Lead   -> base_salary = 85000.0, bonus_rate = 0.90
        #
        # experience_bonus = base_salary * bonus_rate * years_exp / 10.0
        # offered_salary   = base_salary + experience_bonus
        #
        # Set all three fields. Return experience_bonus.
        pass
