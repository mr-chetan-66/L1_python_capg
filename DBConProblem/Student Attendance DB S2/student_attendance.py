### student_attendance.py
### Entity class for StudentAttendance

from datetime import date


class StudentAttendance:

    def __init__(self, attendance_id, student_id, student_name,
                 department, attendance_date, status):
        self.__attendance_id   = attendance_id
        self.__student_id      = student_id
        self.__student_name    = student_name
        self.__department      = department
        self.__attendance_date = attendance_date   # datetime.date object
        self.__status          = status            # 'Present' or 'Absent'

    def get_attendance_id(self):
        return self.__attendance_id

    def set_attendance_id(self, attendance_id):
        self.__attendance_id = attendance_id

    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def get_student_name(self):
        return self.__student_name

    def set_student_name(self, student_name):
        self.__student_name = student_name

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_attendance_date(self):
        return self.__attendance_date

    def set_attendance_date(self, attendance_date):
        self.__attendance_date = attendance_date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
