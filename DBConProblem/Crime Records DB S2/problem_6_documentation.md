# Problem 6 — Crime Record Management System

## Overview

A **multi-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers SELECT across two related tables, ordered exception validation for status updates, date-based case age calculation, dictionary grouping by crime type, and formatted cross-referenced file report writing.

---

## File Structure

```
problem_6_crime/
│
├── database.properties      → DB credentials config
├── crime_record.py          → Entity class (8 fields, getters & setters)
├── officer.py               → Entity class (6 fields, getters & setters)
├── exceptions.py            → 4 custom exception classes
├── crime_dao.py             → Class-based DAO (3 DB methods + status constant)
├── crime_util.py            → Utility helpers (age calc, grouping, display, file export)
└── main.py                  → Entry point (3-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `crime_record.py` | Entity class — 8 fields, getters & setters |
| `officer.py` | Entity class — 6 fields, getters & setters |
| `exceptions.py` | 4 custom exceptions isolated in one place |
| `crime_dao.py` | Class-based DAO — 3 methods: SELECT crimes by location, SELECT officer by ID, UPDATE case status with rollback. Holds `VALID_CASE_STATUSES` constant |
| `crime_util.py` | Helpers — case age calculation, crime type grouping, console display, file report export with officer cross-reference |
| `main.py` | Entry point — 3-step flow: retrieve + group → update status → export report |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_crimes_by_location()` | Case-insensitive LOWER() match; sorted DESC by reported_date; raises `InvalidLocationException` if empty |
| **SELECT** | `retrieve_officer_details()` | Raises `OfficerNotFoundException` if not found |
| **UPDATE** | `update_case_status()` | 3-step ordered validation; `conn.rollback()` on `cx_Oracle.DatabaseError` |

---

## New Concepts vs Problem 8 (Courier Tracking)

| Concept | Details |
|---------|---------|
| **Case-insensitive location search** | `WHERE LOWER(location) = :1` with `location.lower()` |
| **Dictionary grouping** | `group_crimes_by_type()` builds a `{crime_type: [records]}` dict with title-cased keys |
| **3-step ordered validation** | `update_case_status()` checks: exists → not closed → valid new status, in that exact order |
| **Cross-referenced report** | `export_crime_report()` calls `crime_dao.retrieve_officer_details()` per record; gracefully writes "Details not available" on `OfficerNotFoundException` |
| **VALID_CRIME_TYPES in util** | Constant lives in `crime_util.py` since it is used only for grouping validation, not in DAO |
| **VALID_CASE_STATUSES in DAO** | Constant lives in `crime_dao.py` since it is used only in `update_case_status()` |

---

## Oracle Tables

```sql
CREATE TABLE crime_record (
    record_id     NUMBER PRIMARY KEY,
    case_number   VARCHAR2(20),
    crime_type    VARCHAR2(30),
    location      VARCHAR2(100),
    reported_date DATE,
    status        VARCHAR2(30),
    officer_id    NUMBER,
    suspect_name  VARCHAR2(100)
);

CREATE TABLE officer (
    officer_id    NUMBER PRIMARY KEY,
    officer_name  VARCHAR2(100),
    badge_number  VARCHAR2(20),
    rank          VARCHAR2(50),
    department    VARCHAR2(100),
    joining_date  DATE
);
```

---

## Entity Class — `crime_record.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `record_id` | NUMBER | Primary key |
| `case_number` | VARCHAR2(20) | Case reference number e.g. `CR-2024-001` |
| `crime_type` | VARCHAR2(30) | Type of crime — must be in `VALID_CRIME_TYPES` |
| `location` | VARCHAR2(100) | Location / area name |
| `reported_date` | DATE | Date the crime was reported |
| `status` | VARCHAR2(30) | `'Open'`, `'Under Investigation'`, or `'Closed'` |
| `officer_id` | NUMBER | FK → officer table |
| `suspect_name` | VARCHAR2(100) | Suspect name or `'Unknown'` |

All fields are **private** with public getters and setters following encapsulation principles.

---

## Entity Class — `officer.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `officer_id` | NUMBER | Primary key |
| `officer_name` | VARCHAR2(100) | Full name |
| `badge_number` | VARCHAR2(20) | Badge number e.g. `B-1042` |
| `rank` | VARCHAR2(50) | Rank e.g. `Inspector`, `SI`, `DSP` |
| `department` | VARCHAR2(100) | Department name |
| `joining_date` | DATE | Date officer joined the force |

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `InvalidLocationException` | No records found for location OR crime record ID not in DB |
| `InvalidCrimeTypeException` | Unknown crime type in records OR invalid new status value |
| `CaseAlreadyClosedException` | Attempting to update a case already marked `'Closed'` |
| `OfficerNotFoundException` | No officer found for the given officer ID |

---

## DAO Class — `crime_dao.py`

```python
class CrimeDao:
    def __init__(self, conn): ...
```

### Constants (module-level)

```python
VALID_CASE_STATUSES = ['Open', 'Under Investigation', 'Closed']
```

### Methods

#### `retrieve_crimes_by_location(location)`
- Executes `WHERE LOWER(location) = :1` using `location.lower()` for case-insensitive match
- Sorted by `reported_date DESC` (most recent first)
- Safely converts Oracle datetime to `date` using `hasattr(..., 'date')`
- Raises `InvalidLocationException` if no records found
- Returns list of `CrimeRecord` objects

#### `retrieve_officer_details(officer_id)`
- Fetches a single `Officer` object by primary key
- Safely converts Oracle datetime to `date`
- Raises `OfficerNotFoundException` if not found

#### `update_case_status(record_id, new_status)`
- Validates in this **exact order**:
  1. Record exists → `InvalidLocationException` if not
  2. Current status is not `'Closed'` → `CaseAlreadyClosedException` if it is
  3. `new_status` is in `VALID_CASE_STATUSES` → `InvalidCrimeTypeException` if not
- UPDATEs `crime_record.status`, commits
- Calls `conn.rollback()` on `cx_Oracle.DatabaseError`
- Returns `"Case status updated successfully."`

---

## Utility Functions — `crime_util.py`

| Function | Description |
|----------|-------------|
| `calculate_case_age_in_days(reported_date)` | Returns `(date.today() - reported_date).days` as int |
| `group_crimes_by_type(crime_list)` | Returns `{title_cased_type: [CrimeRecord, ...]}` dict; raises `InvalidCrimeTypeException` for unknown types |
| `display_crime_summary(location, grouped)` | Prints grouped crime summary with case age to console |
| `export_crime_report(crime_list, crime_dao, filename)` | Writes formatted report; fetches officer per record via `crime_dao`; writes "Details not available" on `OfficerNotFoundException`; raises `IOError` on write failure |

### VALID_CRIME_TYPES (module-level constant in `crime_util.py`)

```python
VALID_CRIME_TYPES = ['theft', 'assault', 'fraud', 'robbery', 'vandalism', 'murder']
```

---

## Main Program Flow — `main.py`

```
Step 1 — RETRIEVE CRIMES BY LOCATION
    ├── Input: location
    ├── Call: crime_dao.retrieve_crimes_by_location(location)
    ├── Call: util.group_crimes_by_type(crimes)
    └── Display: util.display_crime_summary(location, grouped)

Step 2 — UPDATE CASE STATUS
    ├── Input: record_id, new_status
    ├── Call: crime_dao.update_case_status(record_id, new_status)
    └── Display: result message

Step 3 — EXPORT CRIME REPORT
    ├── Input: filename
    ├── Call: util.export_crime_report(crimes, crime_dao, filename)
    └── Display: confirmation message
```

---

## Sample Run

```
=======================================================
        CRIME RECORD MANAGEMENT SYSTEM
=======================================================

--- RETRIEVE CRIMES BY LOCATION ---
Enter Location to Search : Koramangala

Crime Summary for Location: Koramangala
=======================================================

[Vandalism] - 1 case(s)
  Case No  : CR-2024-006
  Status   : Open
  Suspect  : Unknown
  Reported : 01-07-2024
  Age      : 35 day(s)

[Fraud] - 1 case(s)
  Case No  : CR-2024-003
  Status   : Closed
  Suspect  : Anil Sharma
  Reported : 20-05-2024
  Age      : 77 day(s)

--- UPDATE CASE STATUS ---
Enter Crime Record ID to Update : 1
Enter New Status (Open / Under Investigation / Closed) : Under Investigation
Update Status : Case status updated successfully.

--- EXPORT CRIME REPORT ---
Enter Filename to Export Report : koramangala_crimes.txt
Crime report exported to koramangala_crimes.txt
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Location has no records in DB | `InvalidLocationException` — "No crime records found for the given location." |
| Record ID not in DB | `InvalidLocationException` — "Crime record not found for the given ID." |
| Case is already `'Closed'` | `CaseAlreadyClosedException` — "Case is already closed and cannot be updated." |
| Invalid new status value | `InvalidCrimeTypeException` — "Invalid status. Must be Open, Under Investigation, or Closed." |
| Unknown crime type in records | `InvalidCrimeTypeException` — "Unknown crime type found in records: `<crime_type>`" |
| Officer ID not in DB | `OfficerNotFoundException` in main; in report export writes "Details not available" |
| DB error on UPDATE | `conn.rollback()` called; `cx_Oracle.DatabaseError` re-raised |
| Report file write fails | `IOError` raised from `export_crime_report` |

---

## Key Python Concepts Used

```python
# Case-insensitive location search
WHERE LOWER(location) = :1
cursor.execute(query, (location.lower(),))

# Dictionary grouping with title-cased keys
key = crime_type.title()
if key not in grouped:
    grouped[key] = []
grouped[key].append(rec)

# Case age calculation
(date.today() - reported_date).days

# 3-step ordered validation in update_case_status
if row is None:        raise InvalidLocationException(...)
if status == 'Closed': raise CaseAlreadyClosedException(...)
if new_status not in VALID_CASE_STATUSES: raise InvalidCrimeTypeException(...)

# Graceful officer lookup in export
try:
    officer = crime_dao.retrieve_officer_details(rec.get_officer_id())
    f.write(f"Officer : {officer.get_officer_name()} (Badge: {officer.get_badge_number()})\n")
except OfficerNotFoundException:
    f.write("Officer : Details not available\n")

# Rollback on DB error
except cx_Oracle.DatabaseError:
    self.__conn.rollback()
    raise
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Salary Range | SELECT + BETWEEN |
| 3 | Product Low Stock | SELECT + multi-condition + SYSDATE |
| 4 | Order Placement | INSERT + SELECT |
| 5 | Bank Account Transaction | SELECT + conditional UPDATE |
| **6** | **Crime Record Management** | **Two-table DAO + Custom Exceptions + Dict Grouping + Case Age + Cross-referenced File Report** |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
