# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class JobApplication:
    def __init__(self,application_id:str,job_code:str,applicant_name:str,experience_grade:str,years_exp:int,application_date:date,closing_date:date,job_title:str,status:str):
        self.__application_id=application_id
        self.__job_code=job_code
        self.__applicant_name=applicant_name
        self.__experience_grade=experience_grade
        self.__years_exp=years_exp
        self.__application_date=application_date
        self.__closing_date=closing_date
        self.__job_title=job_title
        self.__status=status
        self.__base_salary=0.0
        self.__experience_bonus=0.0
        self.__offered_salary=0.0

    def get_application_id(self): return self.__application_id
    def get_job_code(self): return self.__job_code
    def get_applicant_name(self): return self.__applicant_name
    def get_experience_grade(self): return self.__experience_grade
    def get_years_exp(self): return self.__years_exp
    def get_application_date(self): return self.__application_date
    def get_closing_date(self): return self.__closing_date
    def get_job_title(self): return self.__job_title
    def get_status(self): return self.__status
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
    def set_status(self, v): self.__status = v
    def set_base_salary(self, v): self.__base_salary = v
    def set_experience_bonus(self, v): self.__experience_bonus = v
    def set_offered_salary(self, v): self.__offered_salary = v

    def calculate_offered_salary(self):
        g=self.__experience_grade
        br=0
        if g=='Junior':
            self.__base_salary=25000.0
            br=0.30   
        elif g=='Mid':
            self.__base_salary=40000.0
            br=0.50   
        elif g=='Senior':
            self.__base_salary=60000.0
            br=0.70   
        elif g=='Lead':
            self.__base_salary=85000.0
            br=0.90  
            
        self.__experience_bonus=self.__base_salary*br*self.__years_exp/10.0
        
        self.__offered_salary=self.__base_salary+self.__experience_bonus
            
                 
