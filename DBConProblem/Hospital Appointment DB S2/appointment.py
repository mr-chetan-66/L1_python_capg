### appointment.py
### Entity class for Appointment

class Appointment:
    def __init__(self, appointment_id, patient_name, doctor_name, department,
                 appointment_date, appointment_time, status):
        self.__appointment_id   = appointment_id
        self.__patient_name     = patient_name
        self.__doctor_name      = doctor_name
        self.__department       = department
        self.__appointment_date = appointment_date   # datetime.date object
        self.__appointment_time = appointment_time   # datetime.time object
        self.__status           = status             # 'Scheduled', 'Completed', 'Cancelled'

    def get_appointment_id(self):
        return self.__appointment_id

    def set_appointment_id(self, appointment_id):
        self.__appointment_id = appointment_id

    def get_patient_name(self):
        return self.__patient_name

    def set_patient_name(self, patient_name):
        self.__patient_name = patient_name

    def get_doctor_name(self):
        return self.__doctor_name

    def set_doctor_name(self, doctor_name):
        self.__doctor_name = doctor_name

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_appointment_date(self):
        return self.__appointment_date

    def set_appointment_date(self, appointment_date):
        self.__appointment_date = appointment_date

    def get_appointment_time(self):
        return self.__appointment_time

    def set_appointment_time(self, appointment_time):
        self.__appointment_time = appointment_time

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
