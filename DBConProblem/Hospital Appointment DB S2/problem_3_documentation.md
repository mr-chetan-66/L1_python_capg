# Problem 3 — Hospital Appointment Management System

## Overview

A **single-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers SELECT with case-insensitive WHERE + ORDER BY on both date and time, dictionary grouping by status, slot conflict checking via a COUNT query, and CSV-style file export.

---

## File Structure

```
problem_3_appointment/
│
├── database.properties      → DB credentials config
├── appointment.py           → Entity class (7 fields, getters & setters)
├── exceptions.py            → 3 custom exception classes
├── appointment_dao.py       → Class-based DAO (2 DB methods + private row mapper)
├── appointment_util.py      → Utility helpers (status grouping, display, file export)
└── main.py                  → Entry point (3-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `appointment.py` | Entity class — 7 fields, getters & setters |
| `exceptions.py` | 3 custom exceptions isolated in one place |
| `appointment_dao.py` | Class-based DAO — 2 public methods: SELECT by doctor, SELECT slot check (COUNT). Private `__map_row_to_appointment()` shared by both |
| `appointment_util.py` | Helpers — status grouping dict, console display, CSV-style file export. Holds `VALID_STATUSES` constant |
| `main.py` | Entry point — 3-step flow: retrieve + group → check slot → export file |

---

## Database Operation Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_appointments_by_doctor()` | Case-insensitive `LOWER()` match; sorted by `appointment_date ASC` then `appointment_time ASC`; raises `InvalidDoctorException` if empty |
| **SELECT COUNT** | `check_slot_availability()` | Counts existing `'Scheduled'` rows for doctor + date + time; raises `AppointmentSlotConflictException` if count > 0; returns `True` if available |

---

## Oracle Table

```sql
CREATE TABLE appointment (
    appointment_id   NUMBER PRIMARY KEY,
    patient_name     VARCHAR2(100),
    doctor_name      VARCHAR2(100),
    department       VARCHAR2(100),
    appointment_date DATE,
    appointment_time VARCHAR2(5),
    status           VARCHAR2(20)
);
```

---

## Entity Class — `appointment.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `appointment_id` | NUMBER | Primary key |
| `patient_name` | VARCHAR2(100) | Full name of the patient |
| `doctor_name` | VARCHAR2(100) | Full name of the doctor |
| `department` | VARCHAR2(100) | Hospital department |
| `appointment_date` | DATE | Date of the appointment |
| `appointment_time` | VARCHAR2(5) | Time in `HH:MM` format |
| `status` | VARCHAR2(20) | `'Scheduled'`, `'Completed'`, or `'Cancelled'` |

All fields are **private** with public getters and setters following encapsulation principles.

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `InvalidDoctorException` | No appointments found for the given doctor name |
| `InvalidStatusException` | Any appointment has a status outside `VALID_STATUSES` |
| `AppointmentSlotConflictException` | A `'Scheduled'` appointment already exists for the doctor at that date and time |

---

## DAO Class — `appointment_dao.py`

```python
class AppointmentDao:
    def __init__(self, conn): ...
```

### Public Methods

#### `retrieve_appointments_by_doctor(doctor_name)`
- Executes `WHERE LOWER(doctor_name) = :1` using `doctor_name.lower()`
- Sorted by `appointment_date ASC`, then `appointment_time ASC`
- Uses `__map_row_to_appointment()` per row
- Raises `InvalidDoctorException` if no records found
- Returns list of `Appointment` objects

#### `check_slot_availability(doctor_name, appointment_date, appointment_time)`
- Executes `SELECT COUNT(*)` checking for an existing `'Scheduled'` record
  at the given doctor + date + time combination
- Formats `appointment_time` as `"%H:%M"` string for comparison against `VARCHAR2(5)` column
- Raises `AppointmentSlotConflictException` if count > 0
- Returns `True` if the slot is free

### Private Method

#### `__map_row_to_appointment(row)`
- Shared by `retrieve_appointments_by_doctor` (used in the row loop)
- Safely converts Oracle DATE → `date` using `hasattr(..., 'date')`
- Safely parses `VARCHAR2` time string → `time` using `datetime.strptime(..., "%H:%M:%S")`; guarded with `isinstance(..., time)`
- Returns an `Appointment` object

---

## Utility Functions — `appointment_util.py`

| Function | Description |
|----------|-------------|
| `group_appointments_by_status(appointment_list)` | Returns `{status: [Appointment, ...]}` dict; raises `InvalidStatusException` for unknown statuses |
| `display_appointment_summary(doctor_name, grouped)` | Prints grouped summary with patient, date, time, dept per appointment |
| `export_appointments_to_file(appointment_list, filename)` | Writes one CSV-style line per appointment; raises `IOError` on write failure |

### VALID_STATUSES (module-level constant in `appointment_util.py`)

```python
VALID_STATUSES = {'Scheduled', 'Completed', 'Cancelled'}
```

### Exported File Format

```
appointment_id,patient_name,doctor_name,department,DD-MM-YYYY,HH:MM,status
```

Example:
```
1001,Ramesh Iyer,Dr. Suresh Menon,Cardiology,10-07-2024,09:00,Scheduled
1002,Kavya Pillai,Dr. Suresh Menon,Cardiology,10-07-2024,09:30,Completed
```

---

## Main Program Flow — `main.py`

```
Step 1 — APPOINTMENTS BY DOCTOR
    ├── Input: doctor_name
    ├── Call: appointment_dao.retrieve_appointments_by_doctor(doctor_name)
    ├── Call: util.group_appointments_by_status(appointments)
    └── Display: util.display_appointment_summary(doctor_name, grouped)

Step 2 — CHECK SLOT AVAILABILITY
    ├── Input: check_date_str (DD-MM-YYYY), check_time_str (HH:MM)
    ├── Parse: datetime.strptime → date + time objects
    ├── Call: appointment_dao.check_slot_availability(doctor_name, check_date, check_time)
    └── Display: "Slot is available." OR AppointmentSlotConflictException message

Step 3 — EXPORT APPOINTMENTS
    ├── Input: filename
    ├── Call: util.export_appointments_to_file(appointments, filename)
    └── Display: confirmation message
```

---

## Sample Run

```
==================================================
    HOSPITAL APPOINTMENT MANAGEMENT SYSTEM
==================================================

--- APPOINTMENTS BY DOCTOR ---
Enter Doctor Name : Dr. Suresh Menon

Appointment Summary for Dr. Dr. Suresh Menon
==================================================

[Scheduled] - 2 appointment(s)
  ID       : 1001
  Patient  : Ramesh Iyer
  Date     : 10-07-2024
  Time     : 09:00
  Dept     : Cardiology

  ID       : 1003
  Patient  : Anand Krishnan
  Date     : 11-07-2024
  Time     : 10:00
  Dept     : Cardiology

[Completed] - 1 appointment(s)
  ID       : 1002
  Patient  : Kavya Pillai
  Date     : 10-07-2024
  Time     : 09:30
  Dept     : Cardiology

[Cancelled] - 1 appointment(s)
  ID       : 1004
  Patient  : Meena Nair
  Date     : 11-07-2024
  Time     : 11:00
  Dept     : Cardiology

--- CHECK SLOT AVAILABILITY ---
Enter Date to Check (DD-MM-YYYY) : 10-07-2024
Enter Time to Check (HH:MM 24-hr): 09:00
Slot already booked for the given doctor at this date and time.

--- EXPORT APPOINTMENTS ---
Enter Filename to Export Appointments : suresh_appointments.txt
Appointments exported successfully to suresh_appointments.txt
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Doctor name has no records in DB | `InvalidDoctorException` — "No appointments found for the given doctor." |
| Any appointment has unrecognised status | `InvalidStatusException` — "Invalid status found in records." |
| Slot already has a `'Scheduled'` appointment | `AppointmentSlotConflictException` — "Slot already booked for the given doctor at this date and time." |
| Slot is free | Returns `True`, prints "Slot is available." |
| Invalid date/time format entered | `ValueError` caught in `main()` — "Invalid date or time format." |
| Export file write fails | `IOError` raised from `export_appointments_to_file` |

---

## Key Python Concepts Used

```python
# Case-insensitive doctor search + ORDER BY two columns
WHERE LOWER(doctor_name) = :1
ORDER BY appointment_date ASC, appointment_time ASC

# Slot conflict check using COUNT(*)
SELECT COUNT(*) FROM appointment
WHERE LOWER(doctor_name) = :1
  AND appointment_date   = :2
  AND appointment_time   = :3
  AND LOWER(status)      = 'scheduled'

# time stored as VARCHAR2 — formatted back for comparison
time_str = appointment_time.strftime("%H:%M")

# Safely parsing Oracle VARCHAR2 time string to Python time object
appt_time = row[5] if isinstance(row[5], time) \
            else datetime.strptime(str(row[5]), "%H:%M:%S").time()

# Dictionary grouping using a set for O(1) lookup
VALID_STATUSES = {'Scheduled', 'Completed', 'Cancelled'}
if status not in VALID_STATUSES:
    raise InvalidStatusException(...)

# User date/time input parsing
check_date = datetime.strptime(check_date_str, "%d-%m-%Y").date()
check_time = datetime.strptime(check_time_str, "%H:%M").time()

# CSV-style file export with strftime formatting
f"{appt.get_appointment_date().strftime('%d-%m-%Y')},"
f"{appt.get_appointment_time().strftime('%H:%M')},"
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Payroll | SELECT + salary dict + experience calc + file report |
| **3** | **Hospital Appointment** | **SELECT + ORDER BY two cols + COUNT slot check + dict grouping + CSV export** |
| 4 | Order Placement | INSERT + SELECT |
| 5 | Event Booking | Two-table DAO + 4-step validation + INSERT+UPDATE transaction + nested dict |
| 6 | Crime Record Management | Two-table DAO + Custom Exceptions + Dict Grouping + File Report |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
