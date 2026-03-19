from datetime import date

POLICY_RATES = {"Platinum": (0.95, 0.05), "Gold": (0.80, 0.20), "Silver": (0.60, 0.40), "Bronze": (0.40, 0.60)}

class InsuranceClaim:
    def __init__(self, claim_id, policy_id, patient_name, policy_type, claim_amount, claim_date, policy_date):
        self.__claim_id = claim_id; self.__policy_id = policy_id
        self.__patient_name = patient_name; self.__policy_type = policy_type
        self.__claim_amount = claim_amount; self.__claim_date = claim_date
        self.__policy_date = policy_date; self.__coverage_amount = 0.0
        self.__deductible = 0.0; self.__approved_amount = 0.0

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
        cov_rate, ded_rate = POLICY_RATES.get(self.__policy_type, (0.40, 0.60))
        cov = self.__claim_amount * cov_rate
        ded = self.__claim_amount * ded_rate
        self.__coverage_amount = cov
        self.__deductible = ded
        self.__approved_amount = cov
        return ded
