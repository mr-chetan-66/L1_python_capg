# Problem — Student Attendance Management System

## Overview

A **SELECT + aggregation** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
Covers database querying with date range filtering, percentage calculation, custom exception handling, and file export.

---

## File Structure

```
attendance_problem/
│
├── database.properties          → DB credentials config
├── student_attendance.py        → Entity class (6 fields, getters & setters)
├── attendance_dao.py            → Class-based DAO (2 DB methods) + custom exception
├── attendance_util.py           → Utility helpers (validation, display, calculations, export)
└── main.py                      → Entry point (3-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `student_attendance.py` | Entity class — 6 fields, getters & setters |
| `attendance_dao.py` | Class-based DAO — 2 methods: date-range SELECT with custom exception, percentage aggregation SELECT |
| `attendance_util.py` | Helpers — validation, display, count/present/absent aggregators, most recent record, status label, file export |
| `main.py` | Entry point — 3-step flow: view records → calculate percentage → export to file |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_attendance_by_date_range()` | Filters by department (case-insensitive) + BETWEEN dates, ordered by date ASC |
| **SELECT** | `calculate_attendance_percentage()` | Aggregates COUNT + SUM(CASE) in one query, returns -1 if student not found |

---

## Oracle Table

```sql
CREATE TABLE attendance (
    attendance_id    NUMBER PRIMARY KEY,
    student_id       NUMBER,
    student_name     VARCHAR2(100),
    department       VARCHAR2(100),
    attendance_date  DATE,
    status           VARCHAR2(10)
);
```

### Sample Records

| attendance_id | student_id | student_name | department       | attendance_date | status  |
|---------------|------------|--------------|------------------|-----------------|---------|
| 1             | 201        | Arun Kumar   | Computer Science | 01-07-2024      | Present |
| 2             | 202        | Priya Sharma | Computer Science | 01-07-2024      | Absent  |
| 3             | 201        | Arun Kumar   | Computer Science | 02-07-2024      | Present |
| 4             | 203        | Rohit Verma  | Electronics      | 01-07-2024      | Present |
| 5             | 202        | Priya Sharma | Computer Science | 02-07-2024      | Present |
| 6             | 201        | Arun Kumar   | Computer Science | 03-07-2024      | Absent  |

---

## Entity Class — `student_attendance.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `attendance_id` | NUMBER | Primary key |
| `student_id` | NUMBER | ID of the student |
| `student_name` | VARCHAR2(100) | Full name of the student |
| `department` | VARCHAR2(100) | Department name |
| `attendance_date` | DATE | Date of attendance |
| `status` | VARCHAR2(10) | `'Present'` or `'Absent'` |

All fields are **private** with public getters and setters following encapsulation principles.

---

## DAO Class — `attendance_dao.py`

```python
class AttendanceDao:
    def __init__(self, conn): ...
```

### Custom Exception

```python
class InvalidDepartmentException(Exception):
    pass
```
Defined in `attendance_dao.py` and imported into `main.py` directly.

### Methods

#### `retrieve_attendance_by_date_range(department, from_date, to_date)`
- Queries attendance table with `LOWER(department) = :1` for case-insensitive match
- Uses `BETWEEN :2 AND :3` for inclusive date range filtering
- Results ordered by `attendance_date ASC`
- Returns list of `StudentAttendance` objects
- Raises `InvalidDepartmentException` with message `"No records found for the given department and date range."` if no rows returned

#### `calculate_attendance_percentage(student_id)`
- Runs a single aggregation query: `COUNT(*)` and `SUM(CASE WHEN LOWER(status) = 'present' THEN 1 ELSE 0 END)`
- Formula: `round((present / total) * 100, 2)`
- Returns `-1` if total is 0 (student not found)
- Returns `float` attendance percentage

---

## Utility Functions — `attendance_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_student_id(id)` | Returns `True` if `id > 0` |
| `is_valid_date_range(from, to)` | Returns `True` if `to >= from` |
| `display_attendance(record)` | Prints all attendance fields with aligned labels |
| `get_result_count(list)` | Returns length of attendance list |
| `get_present_count(list)` | Returns count of `'Present'` records using sum + lambda |
| `get_absent_count(list)` | Returns count of `'Absent'` records using sum + lambda |
| `get_most_recent_record(list)` | Returns record with latest date using `lambda` + `max()` |
| `get_status_label(record)` | Returns `"✔ Present"` or `"✗ Absent"` |
| `export_to_file(list, filename)` | Writes records to file in CSV format, raises `IOError` on failure |

---

## Main Program Flow — `main.py`

```
Step 1 — VIEW ATTENDANCE BY DEPARTMENT
    ├── Input: department, from_date, to_date (DD-MM-YYYY)
    ├── Validate: date range
    ├── Call: attendance_dao.retrieve_attendance_by_date_range(...)
    ├── Catch: InvalidDepartmentException → print message and return
    └── Display: count, present, absent, most recent date, each record with label

Step 2 — ATTENDANCE PERCENTAGE
    ├── Input: student_id
    ├── Validate: is_valid_student_id
    ├── Call: attendance_dao.calculate_attendance_percentage(student_id)
    └── Display: percentage or "No records found" if -1

Step 3 — EXPORT TO FILE
    ├── Input: filename
    ├── Call: util.export_to_file(attendance_list, filename)
    └── Display: success message or IOError message
```

---

## Sample Run

```
==========================================
     STUDENT ATTENDANCE MANAGEMENT SYSTEM
==========================================

--- VIEW ATTENDANCE BY DEPARTMENT ---
Enter Department              : Computer Science
Enter From Date (DD-MM-YYYY)  : 01-07-2024
Enter To Date   (DD-MM-YYYY)  : 03-07-2024

Attendance Records:
Total Records  : 5
Total Present  : 4
Total Absent   : 1
Most Recent Date: 03-07-2024
------------------------------------------
Attendance ID  : 1
Student ID     : 201
Student Name   : Arun Kumar
Department     : Computer Science
Date           : 01-07-2024
Status         : Present
------------------------------------------
Status Label   : ✔ Present
------------------------------------------

--- ATTENDANCE PERCENTAGE ---
Enter Student ID : 201
Attendance Percentage: 66.67%

--- EXPORT TO FILE ---
Enter Filename to Export (e.g. attendance.txt) : cs_attendance.txt
Records exported successfully to cs_attendance.txt
```

### Exported File Format (`cs_attendance.txt`)

```
1,201,Arun Kumar,Computer Science,01-07-2024,Present
2,202,Priya Sharma,Computer Science,01-07-2024,Absent
3,201,Arun Kumar,Computer Science,02-07-2024,Present
5,202,Priya Sharma,Computer Science,02-07-2024,Present
6,201,Arun Kumar,Computer Science,03-07-2024,Absent
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Department with no records | `InvalidDepartmentException` → prints message, program ends |
| `to_date < from_date` | `"To Date Must Be On Or After From Date"` |
| Invalid date format input | `"Invalid date format. Please use DD-MM-YYYY."` (caught by `ValueError`) |
| Student ID not found | Returns `-1` → prints `"No records found for the given student ID"` |
| File export failure | `IOError` caught → prints `"Export Failed: ..."` |
| `student_id <= 0` | `"Invalid Student ID"` |

---

## Key Python Concepts Used

```python
# Case-insensitive department match with positional bind variables
cursor.execute(query, (department.lower(), from_date, to_date))

# Single aggregation query for percentage
SUM(CASE WHEN LOWER(status) = 'present' THEN 1 ELSE 0 END)

# Custom exception raised inside DAO
raise InvalidDepartmentException("No records found...")

# Date parsing from DD-MM-YYYY format
from_date = datetime.strptime(from_date_str, "%d-%m-%Y").date()

# Lambda for finding most recent record
max(attendance_list, key=lambda r: r.get_attendance_date())

# Oracle datetime vs date safety handling
att_date = att_date.date() if hasattr(att_date, 'date') else att_date

# File export with IOError handling
except IOError as e:
    raise IOError(f"Failed to write file: {e}")
```

---

## Concepts Covered

| Concept | Where Used |
|---------|------------|
| DB Connectivity | Oracle connection via `db_config.py`, SELECT with date range and WHERE clause |
| Date / Time Manipulation | `datetime.strptime`, `.strftime`, `BETWEEN` in SQL, Oracle date safety |
| Custom Exception | `InvalidDepartmentException` defined in DAO, caught in `main.py` |
| File Handling | Writing CSV-format records to `.txt` file in `attendance_util.py` |
| Collections | List of `StudentAttendance` objects, aggregation with `sum()` + `lambda` |
| Class-based DAO | `AttendanceDao` with `__conn`, methods encapsulate all DB logic |
| Encapsulation | All entity fields private, accessed only via getters/setters |
