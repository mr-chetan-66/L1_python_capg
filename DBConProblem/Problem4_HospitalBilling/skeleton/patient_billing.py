# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class PatientBilling:

    # Define the parameterized constructor here
    # Parameters: bill_id, patient_id, date_of_admission, ward_type,
    #             date_of_discharge, no_of_days, treatment_code, insurance_status
    # Default values for remaining attributes: 0.0
    def __init__(self, bill_id: str, patient_id: str, date_of_admission: date,
                 ward_type: str, date_of_discharge: date, no_of_days: int,
                 treatment_code: str, insurance_status: str):
        # Write your code here
        pass

    # Write all getters and setters for the private attributes below

    def get_bill_id(self):
        pass

    def set_bill_id(self, bill_id):
        pass

    def get_patient_id(self):
        pass

    def set_patient_id(self, patient_id):
        pass

    def get_date_of_admission(self):
        pass

    def set_date_of_admission(self, date_of_admission):
        pass

    def get_ward_type(self):
        pass

    def set_ward_type(self, ward_type):
        pass

    def get_date_of_discharge(self):
        pass

    def set_date_of_discharge(self, date_of_discharge):
        pass

    def get_no_of_days(self):
        pass

    def set_no_of_days(self, no_of_days):
        pass

    def get_treatment_code(self):
        pass

    def set_treatment_code(self, treatment_code):
        pass

    def get_insurance_status(self):
        pass

    def set_insurance_status(self, insurance_status):
        pass

    def get_bed_charges(self):
        pass

    def set_bed_charges(self, bed_charges):
        pass

    def get_treatment_charges(self):
        pass

    def set_treatment_charges(self, treatment_charges):
        pass

    def get_nursing_charges(self):
        pass

    def set_nursing_charges(self, nursing_charges):
        pass

    def get_discount(self):
        pass

    def set_discount(self, discount):
        pass

    def get_total_bill_amount(self):
        pass

    def set_total_bill_amount(self, total_bill_amount):
        pass
