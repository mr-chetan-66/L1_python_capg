from datetime import date

class PatientBilling:

    def __init__(self, bill_id: str, patient_id: str, date_of_admission: date,
                 ward_type: str, date_of_discharge: date, no_of_days: int,
                 treatment_code: str, insurance_status: str):
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        self.__date_of_admission = date_of_admission
        self.__ward_type = ward_type
        self.__date_of_discharge = date_of_discharge
        self.__no_of_days = no_of_days
        self.__treatment_code = treatment_code
        self.__insurance_status = insurance_status
        self.__bed_charges = 0.0
        self.__treatment_charges = 0.0
        self.__nursing_charges = 0.0
        self.__discount = 0.0
        self.__total_bill_amount = 0.0

    def get_bill_id(self):
        return self.__bill_id

    def set_bill_id(self, bill_id):
        self.__bill_id = bill_id

    def get_patient_id(self):
        return self.__patient_id

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def get_date_of_admission(self):
        return self.__date_of_admission

    def set_date_of_admission(self, date_of_admission):
        self.__date_of_admission = date_of_admission

    def get_ward_type(self):
        return self.__ward_type

    def set_ward_type(self, ward_type):
        self.__ward_type = ward_type

    def get_date_of_discharge(self):
        return self.__date_of_discharge

    def set_date_of_discharge(self, date_of_discharge):
        self.__date_of_discharge = date_of_discharge

    def get_no_of_days(self):
        return self.__no_of_days

    def set_no_of_days(self, no_of_days):
        self.__no_of_days = no_of_days

    def get_treatment_code(self):
        return self.__treatment_code

    def set_treatment_code(self, treatment_code):
        self.__treatment_code = treatment_code

    def get_insurance_status(self):
        return self.__insurance_status

    def set_insurance_status(self, insurance_status):
        self.__insurance_status = insurance_status

    def get_bed_charges(self):
        return self.__bed_charges

    def set_bed_charges(self, bed_charges):
        self.__bed_charges = bed_charges

    def get_treatment_charges(self):
        return self.__treatment_charges

    def set_treatment_charges(self, treatment_charges):
        self.__treatment_charges = treatment_charges

    def get_nursing_charges(self):
        return self.__nursing_charges

    def set_nursing_charges(self, nursing_charges):
        self.__nursing_charges = nursing_charges

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    def get_total_bill_amount(self):
        return self.__total_bill_amount

    def set_total_bill_amount(self, total_bill_amount):
        self.__total_bill_amount = total_bill_amount
