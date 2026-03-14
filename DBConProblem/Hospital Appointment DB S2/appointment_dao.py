### appointment_dao.py
### Data Access Object Class — all DB operations for Appointment
### Class-based DAO with SELECT (by doctor) and SELECT (slot check)

import appointment as ap
import cx_Oracle
from datetime import datetime, time
from exceptions import InvalidDoctorException, AppointmentSlotConflictException


class AppointmentDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all appointments for a given doctor
    # ----------------------------------------------------------------
    def retrieve_appointments_by_doctor(self, doctor_name):
        cursor = self.__conn.cursor()

        query = """
            SELECT appointment_id, patient_name, doctor_name, department,
                   appointment_date, appointment_time, status
            FROM appointment
            WHERE LOWER(doctor_name) = :1
            ORDER BY appointment_date ASC, appointment_time ASC
        """

        cursor.execute(query, (doctor_name.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise InvalidDoctorException(
                "No appointments found for the given doctor.")

        appt_list = []
        for row in rows:
            appt_obj = self.__map_row_to_appointment(row)
            appt_list.append(appt_obj)

        return appt_list

    # ----------------------------------------------------------------
    # SELECT — check if a time slot is already booked for a doctor
    # ----------------------------------------------------------------
    def check_slot_availability(self, doctor_name, appointment_date, appointment_time):
        cursor = self.__conn.cursor()

        query = """
            SELECT COUNT(*) FROM appointment
            WHERE LOWER(doctor_name) = :1
              AND appointment_date    = :2
              AND appointment_time    = :3
              AND LOWER(status)       = 'scheduled'
        """

        # appointment_time stored as VARCHAR2(5) — format to HH:MM for comparison
        time_str = appointment_time.strftime("%H:%M")
        cursor.execute(query, (doctor_name.lower(), appointment_date, time_str))
        count = cursor.fetchone()[0]
        cursor.close()

        if count > 0:
            raise AppointmentSlotConflictException(
                "Slot already booked for the given doctor at this date and time.")

        return True

    # ----------------------------------------------------------------
    # PRIVATE — shared row-to-Appointment mapping for both SELECT methods
    # ----------------------------------------------------------------
    def __map_row_to_appointment(self, row):
        # Safely handle Oracle DATE vs Python date
        appt_date = row[4].date() if hasattr(row[4], 'date') else row[4]

        # Safely handle Oracle VARCHAR2 time string vs Python time object
        appt_time = row[5] if isinstance(row[5], time) \
                    else datetime.strptime(str(row[5]), "%H:%M:%S").time()

        return ap.Appointment(row[0], row[1], row[2], row[3],
                              appt_date, appt_time, row[6])
