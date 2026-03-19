# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class InsuranceClaim:

    def __init__(self, claim_id:str, policy_id:str, patient_name:str,
                 policy_type:str, claim_amount:float, claim_date:date, policy_date:date):
        self.__claim_id = claim_id
        self.__policy_id = policy_id
        self.__patient_name = patient_name
        self.__policy_type = policy_type
        self.__claim_amount = claim_amount
        self.__claim_date = claim_date
        self.__policy_date = policy_date
        self.__coverage_amount = 0.0
        self.__deductible = 0.0
        self.__approved_amount = 0.0

    def get_claim_id(self): return self.__claim_id
    def get_policy_id(self): return self.__policy_id
    def get_patient_name(self): return self.__patient_name
    def get_policy_type(self): return self.__policy_type
    def get_claim_amount(self): return self.__claim_amount
    def get_claim_date(self): return self.__claim_date
    def get_policy_date(self): return self.__policy_date
    def get_coverage_amount(self): return self.__coverage_amount
    def get_deductible(self): return self.__deductible
    def get_approved_amount(self): return self.__approved_amount

    def set_claim_id(self, v): self.__claim_id = v
    def set_policy_id(self, v): self.__policy_id = v
    def set_patient_name(self, v): self.__patient_name = v
    def set_policy_type(self, v): self.__policy_type = v
    def set_claim_amount(self, v): self.__claim_amount = v
    def set_claim_date(self, v): self.__claim_date = v
    def set_policy_date(self, v): self.__policy_date = v
    def set_coverage_amount(self, v): self.__coverage_amount = v
    def set_deductible(self, v): self.__deductible = v
    def set_approved_amount(self, v): self.__approved_amount = v

    def calculate_approved_amount(self):
        # Write your code here
        # Business Rule — Coverage % and Deductible by policy_type:
        #   Platinum -> coverage = 95%, deductible = claim_amount * 0.05
        #   Gold     -> coverage = 80%, deductible = claim_amount * 0.20
        #   Silver   -> coverage = 60%, deductible = claim_amount * 0.40
        #   Bronze   -> coverage = 40%, deductible = claim_amount * 0.60
        #
        # coverage_amount = claim_amount * coverage_rate
        # deductible      = claim_amount * deductible_rate
        # approved_amount = coverage_amount   (i.e. claim_amount - deductible)
        #
        # Set all three fields. Return deductible.
        pass
