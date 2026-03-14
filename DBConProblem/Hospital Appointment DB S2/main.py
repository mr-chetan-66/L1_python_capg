### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import appointment_dao as dao_module
import appointment_util as util
from datetime import datetime
from exceptions import (InvalidDoctorException,
                        InvalidStatusException,
                        AppointmentSlotConflictException)


def main():
    conn             = db.get_connection()
    appointment_dao  = dao_module.AppointmentDao(conn)

    print("=" * 50)
    print("    HOSPITAL APPOINTMENT MANAGEMENT SYSTEM")
    print("=" * 50)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve all appointments for a doctor and display grouped summary
    # ----------------------------------------------------------------
    print("\n--- APPOINTMENTS BY DOCTOR ---")

    doctor_name  = input("Enter Doctor Name : ")
    appointments = appointment_dao.retrieve_appointments_by_doctor(doctor_name)

    try:
        grouped = util.group_appointments_by_status(appointments)
        util.display_appointment_summary(doctor_name, grouped)
    except InvalidStatusException as e:
        print(e)

    # ----------------------------------------------------------------
    # STEP 2 — Check slot availability for the doctor on a given date/time
    # ----------------------------------------------------------------
    print("\n--- CHECK SLOT AVAILABILITY ---")

    check_date_str = input("Enter Date to Check (DD-MM-YYYY) : ")
    check_time_str = input("Enter Time to Check (HH:MM 24-hr): ")

    check_date = datetime.strptime(check_date_str, "%d-%m-%Y").date()
    check_time = datetime.strptime(check_time_str, "%H:%M").time()

    try:
        available = appointment_dao.check_slot_availability(
            doctor_name, check_date, check_time
        )
        if available:
            print("Slot is available.")
    except AppointmentSlotConflictException as e:
        print(e)

    # ----------------------------------------------------------------
    # STEP 3 — Export all appointments to a CSV-style text file
    # ----------------------------------------------------------------
    print("\n--- EXPORT APPOINTMENTS ---")

    filename = input("Enter Filename to Export Appointments : ")

    util.export_appointments_to_file(appointments, filename)
    print(f"Appointments exported successfully to {filename}")


if __name__ == '__main__':
    try:
        main()
    except InvalidDoctorException as e:
        print(e)
    except InvalidStatusException as e:
        print(e)
    except ValueError:
        print("Invalid date or time format.")
