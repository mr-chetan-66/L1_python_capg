### attendance_util.py
### Utility / helper functions for Attendance — validation, display, calculations and file export

VALID_STATUSES = ['present', 'absent']


def is_valid_student_id(student_id):
    # Returns True only if student_id is a positive integer
    return student_id > 0


def is_valid_date_range(from_date, to_date):
    # Returns True only if to_date is on or after from_date
    return to_date >= from_date


def display_attendance(record):
    # Safely handle Oracle datetime vs plain date
    att_date = record.get_attendance_date()
    att_date = att_date.date() if hasattr(att_date, 'date') else att_date

    print("Attendance ID  :", record.get_attendance_id())
    print("Student ID     :", record.get_student_id())
    print("Student Name   :", record.get_student_name())
    print("Department     :", record.get_department())
    print("Date           :", att_date.strftime('%d-%m-%Y'))
    print("Status         :", record.get_status())
    print("-" * 42)


def get_result_count(attendance_list):
    # Returns total number of records in the list
    return len(attendance_list)


def get_present_count(attendance_list):
    # Returns count of records where status is 'Present'
    return sum(1 for r in attendance_list if r.get_status().lower() == 'present')


def get_absent_count(attendance_list):
    # Returns count of records where status is 'Absent'
    return sum(1 for r in attendance_list if r.get_status().lower() == 'absent')


def get_most_recent_record(attendance_list):
    # Returns the StudentAttendance object with the latest attendance_date
    # Returns None if list is empty
    if not attendance_list:
        return None
    return max(attendance_list, key=lambda r: (
        r.get_attendance_date().date()
        if hasattr(r.get_attendance_date(), 'date')
        else r.get_attendance_date()
    ))


def get_status_label(record):
    # Returns a formatted label based on attendance status
    status = record.get_status()
    if status.lower() == 'present':
        return "✔ Present"
    return "✗ Absent"


def export_to_file(attendance_list, filename):
    # Writes each attendance record to a text file
    # Format per line: attendance_id,student_id,student_name,department,DD-MM-YYYY,status
    # Raises IOError if file cannot be created
    try:
        with open(filename, 'w') as f:
            for record in attendance_list:
                att_date = record.get_attendance_date()
                att_date = att_date.date() if hasattr(att_date, 'date') else att_date

                line = (
                    f"{record.get_attendance_id()},"
                    f"{record.get_student_id()},"
                    f"{record.get_student_name()},"
                    f"{record.get_department()},"
                    f"{att_date.strftime('%d-%m-%Y')},"
                    f"{record.get_status()}\n"
                )
                f.write(line)
    except IOError as e:
        raise IOError(f"Failed to write file: {e}")
