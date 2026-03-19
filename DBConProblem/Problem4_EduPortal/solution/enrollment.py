from datetime import date

class Enrollment:
    def __init__(self, enrollment_id:str, course_code:str, student_name:str,
                 grade_level:str, duration_days:int, start_date:date,
                 registration_date:date, course_name:str):
        self.__enrollment_id = enrollment_id
        self.__course_code = course_code
        self.__student_name = student_name
        self.__grade_level = grade_level
        self.__duration_days = duration_days
        self.__start_date = start_date
        self.__registration_date = registration_date
        self.__course_name = course_name
        self.__base_fee = 0.0
        self.__scholarship_amount = 0.0
        self.__payable_fee = 0.0

    def get_enrollment_id(self): return self.__enrollment_id
    def get_course_code(self): return self.__course_code
    def get_student_name(self): return self.__student_name
    def get_grade_level(self): return self.__grade_level
    def get_duration_days(self): return self.__duration_days
    def get_start_date(self): return self.__start_date
    def get_registration_date(self): return self.__registration_date
    def get_course_name(self): return self.__course_name
    def get_base_fee(self): return self.__base_fee
    def get_scholarship_amount(self): return self.__scholarship_amount
    def get_payable_fee(self): return self.__payable_fee

    def set_enrollment_id(self, v): self.__enrollment_id = v
    def set_course_code(self, v): self.__course_code = v
    def set_student_name(self, v): self.__student_name = v
    def set_grade_level(self, v): self.__grade_level = v
    def set_duration_days(self, v): self.__duration_days = v
    def set_start_date(self, v): self.__start_date = v
    def set_registration_date(self, v): self.__registration_date = v
    def set_course_name(self, v): self.__course_name = v
    def set_base_fee(self, v): self.__base_fee = v
    def set_scholarship_amount(self, v): self.__scholarship_amount = v
    def set_payable_fee(self, v): self.__payable_fee = v

    def calculate_fee(self):
        d = self.__duration_days
        if d <= 30:
            base = d * 500.0
        elif d <= 60:
            base = d * 800.0
        else:
            base = d * 1200.0

        lvl = self.__grade_level
        if lvl in ["Level01", "Level02"]:
            rate = 0.20
        elif lvl in ["Level03", "Level04"]:
            rate = 0.10
        else:
            rate = 0.05

        scholarship = base * rate
        payable = base - scholarship
        self.__base_fee = base
        self.__scholarship_amount = scholarship
        self.__payable_fee = payable
        return scholarship
