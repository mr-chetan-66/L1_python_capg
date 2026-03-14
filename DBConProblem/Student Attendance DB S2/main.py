### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import attendance_dao as dao_module
import attendance_util as util
from datetime import datetime
from attendance_dao import InvalidDepartmentException


def main():
    conn           = db.get_connection()
    attendance_dao = dao_module.AttendanceDao(conn)

    print("=" * 42)
    print("     STUDENT ATTENDANCE MANAGEMENT SYSTEM")
    print("=" * 42)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve attendance records by department and date range
    # ----------------------------------------------------------------
    print("\n--- VIEW ATTENDANCE BY DEPARTMENT ---")

    department    = input("Enter Department              : ")
    from_date_str = input("Enter From Date (DD-MM-YYYY)  : ")
    to_date_str   = input("Enter To Date   (DD-MM-YYYY)  : ")

    try:
        from_date = datetime.strptime(from_date_str, "%d-%m-%Y").date()
        to_date   = datetime.strptime(to_date_str,   "%d-%m-%Y").date()
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return

    if not util.is_valid_date_range(from_date, to_date):
        print("To Date Must Be On Or After From Date")
        return

    try:
        attendance_list = attendance_dao.retrieve_attendance_by_date_range(
            department, from_date, to_date
        )
    except InvalidDepartmentException as e:
        print(e)
        return

    print("\nAttendance Records:")
    print("Total Records  :", util.get_result_count(attendance_list))
    print("Total Present  :", util.get_present_count(attendance_list))
    print("Total Absent   :", util.get_absent_count(attendance_list))

    most_recent = util.get_most_recent_record(attendance_list)
    if most_recent:
        att_date = most_recent.get_attendance_date()
        att_date = att_date.date() if hasattr(att_date, 'date') else att_date
        print("Most Recent Date:", att_date.strftime('%d-%m-%Y'))

    print("-" * 42)

    for record in attendance_list:
        util.display_attendance(record)
        print("Status Label   :", util.get_status_label(record))
        print("-" * 42)

    # ----------------------------------------------------------------
    # STEP 2 — Calculate attendance percentage for a student
    # ----------------------------------------------------------------
    print("\n--- ATTENDANCE PERCENTAGE ---")
    student_id = int(input("Enter Student ID : "))

    if not util.is_valid_student_id(student_id):
        print("Invalid Student ID")
        return

    percentage = attendance_dao.calculate_attendance_percentage(student_id)

    if percentage == -1:
        print("No records found for the given student ID")
    else:
        print(f"Attendance Percentage: {percentage}%")

    # ----------------------------------------------------------------
    # STEP 3 — Export attendance records to a file
    # ----------------------------------------------------------------
    print("\n--- EXPORT TO FILE ---")
    filename = input("Enter Filename to Export (e.g. attendance.txt) : ")

    try:
        util.export_to_file(attendance_list, filename)
        print(f"Records exported successfully to {filename}")
    except IOError as e:
        print(f"Export Failed: {e}")


if __name__ == '__main__':
    main()
