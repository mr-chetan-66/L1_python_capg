### appointment_util.py
### Utility / helper functions for Appointment Management — grouping, display, file export

from exceptions import InvalidStatusException

# Valid appointment statuses — used for grouping validation
VALID_STATUSES = {'Scheduled', 'Completed', 'Cancelled'}


# ----------------------------------------------------------------
# GROUPING — group a list of Appointments by status into a dict
# ----------------------------------------------------------------
def group_appointments_by_status(appointment_list):
    # Keys are exact status strings: 'Scheduled', 'Completed', 'Cancelled'
    # Only statuses with at least one appointment appear as keys
    # Raises InvalidStatusException for any unrecognised status
    grouped = {}
    for appt in appointment_list:
        status = appt.get_status()
        if status not in VALID_STATUSES:
            raise InvalidStatusException("Invalid status found in records.")
        if status not in grouped:
            grouped[status] = []
        grouped[status].append(appt)
    return grouped


# ----------------------------------------------------------------
# DISPLAY — print grouped appointment summary to console
# ----------------------------------------------------------------
def display_appointment_summary(doctor_name, grouped):
    print(f"\nAppointment Summary for Dr. {doctor_name}")
    print("=" * 50)
    for status, appt_list in grouped.items():
        print(f"\n[{status}] - {len(appt_list)} appointment(s)")
        for appt in appt_list:
            print(f"  ID       : {appt.get_appointment_id()}")
            print(f"  Patient  : {appt.get_patient_name()}")
            print(f"  Date     : {appt.get_appointment_date().strftime('%d-%m-%Y')}")
            print(f"  Time     : {appt.get_appointment_time().strftime('%H:%M')}")
            print(f"  Dept     : {appt.get_department()}")
            print()


# ----------------------------------------------------------------
# FILE WRITE — export appointments as CSV-style lines to text file
# ----------------------------------------------------------------
def export_appointments_to_file(appointment_list, filename):
    # Format per line:
    # appointment_id,patient_name,doctor_name,department,DD-MM-YYYY,HH:MM,status
    try:
        with open(filename, 'w') as f:
            for appt in appointment_list:
                line = (
                    f"{appt.get_appointment_id()},"
                    f"{appt.get_patient_name()},"
                    f"{appt.get_doctor_name()},"
                    f"{appt.get_department()},"
                    f"{appt.get_appointment_date().strftime('%d-%m-%Y')},"
                    f"{appt.get_appointment_time().strftime('%H:%M')},"
                    f"{appt.get_status()}\n"
                )
                f.write(line)

    except IOError as e:
        raise IOError(f"Failed to write file: {e}")
