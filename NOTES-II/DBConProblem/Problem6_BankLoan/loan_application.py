# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class LoanApplication:

    def __init__(self,loan_id:str,applicant_id:str,date_of_application:date,loan_type:str,date_of_disbursement:date,loan_amount:float,tenure_in_months:int,credit_score:int,loan_status:str,
    ):
        self.__loan_id = loan_id
        self.__applicant_id = applicant_id
        self.__date_of_application = date_of_application
        self.__loan_type = loan_type
        self.__date_of_disbursement = date_of_disbursement
        self.__loan_amount = loan_amount
        self.__tenure_in_months = tenure_in_months
        self.__credit_score = credit_score
        self.__loan_status = loan_status
        self.__annual_interest_rate = 0.0
        self.__processing_fee = 0.0
        self.__monthly_emi = 0.0
        self.__total_interest = 0.0
        self.__total_repayment = 0.0

    def get_loan_id(self):
        return self.__loan_id

    def set_loan_id(self, loan_id):
        self.__loan_id = loan_id

    def get_applicant_id(self):
        return self.__applicant_id

    def set_applicant_id(self, applicant_id):
        self.__applicant_id = applicant_id

    def get_date_of_application(self):
        return self.__date_of_application

    def set_date_of_application(self, date_of_application):
        self.__date_of_application = date_of_application

    def get_loan_type(self):
        return self.__loan_type

    def set_loan_type(self, loan_type):
        self.__loan_type = loan_type

    def get_date_of_disbursement(self):
        return self.__date_of_disbursement

    def set_date_of_disbursement(self, date_of_disbursement):
        self.__date_of_disbursement = date_of_disbursement

    def get_loan_amount(self):
        return self.__loan_amount

    def set_loan_amount(self, loan_amount):
        self.__loan_amount = loan_amount

    def get_tenure_in_months(self):
        return self.__tenure_in_months

    def set_tenure_in_months(self, tenure_in_months):
        self.__tenure_in_months = tenure_in_months

    def get_credit_score(self):
        return self.__credit_score

    def set_credit_score(self, credit_score):
        self.__credit_score = credit_score

    def get_loan_status(self):
        return self.__loan_status

    def set_loan_status(self, loan_status):
        self.__loan_status = loan_status

    def get_annual_interest_rate(self):
        return self.__annual_interest_rate

    def set_annual_interest_rate(self, annual_interest_rate):
        self.__annual_interest_rate = annual_interest_rate

    def get_processing_fee(self):
        return self.__processing_fee

    def set_processing_fee(self, processing_fee):
        self.__processing_fee = processing_fee

    def get_monthly_emi(self):
        return self.__monthly_emi

    def set_monthly_emi(self, monthly_emi):
        self.__monthly_emi = monthly_emi

    def get_total_interest(self):
        return self.__total_interest

    def set_total_interest(self, total_interest):
        self.__total_interest = total_interest

    def get_total_repayment(self):
        return self.__total_repayment

    def set_total_repayment(self, total_repayment):
        self.__total_repayment = total_repayment
