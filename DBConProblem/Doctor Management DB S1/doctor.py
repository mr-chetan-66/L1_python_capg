### doctor.py
### Entity class for Doctor

class Doctor:
    def __init__(self, doctor_id, name, specialization, hospital, experience_years, consultation_fee):
        self.__doctor_id        = doctor_id
        self.__name             = name
        self.__specialization   = specialization
        self.__hospital         = hospital
        self.__experience_years = experience_years
        self.__consultation_fee = consultation_fee

    def get_doctor_id(self):
        return self.__doctor_id

    def set_doctor_id(self, doctor_id):
        self.__doctor_id = doctor_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_specialization(self):
        return self.__specialization

    def set_specialization(self, specialization):
        self.__specialization = specialization

    def get_hospital(self):
        return self.__hospital

    def set_hospital(self, hospital):
        self.__hospital = hospital

    def get_experience_years(self):
        return self.__experience_years

    def set_experience_years(self, experience_years):
        self.__experience_years = experience_years

    def get_consultation_fee(self):
        return self.__consultation_fee

    def set_consultation_fee(self, consultation_fee):
        self.__consultation_fee = consultation_fee
