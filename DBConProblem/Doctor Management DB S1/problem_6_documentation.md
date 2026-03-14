# Problem 6 — Doctor Search System

## Overview

A Python + Oracle Database problem focused on **multi-filter SELECT** with two WHERE conditions, combined with **Python-side analytics** using `lambda` to find the most affordable and most experienced doctor from the result list.

---

## File Structure

```
problem_6_doctor/
│
├── database.properties    → DB credentials config
├── doctor.py              → Entity class (6 fields, getters & setters)
├── doctor_dao.py          → DAO (2 DB functions)
├── doctor_util.py         → Utility helpers (validation, display, analytics)
└── main.py                → Entry point (single search flow with highlights)
```

---

## Oracle Table

```sql
CREATE TABLE doctor (
    doctor_id        VARCHAR2(20) PRIMARY KEY,
    name             VARCHAR2(100),
    specialization   VARCHAR2(100),
    hospital         VARCHAR2(100),
    experience_years NUMBER,
    consultation_fee NUMBER(10,2)
);
```

---

## Entity Class — `doctor.py`

| Field | Type | Description |
|-------|------|-------------|
| `doctor_id` | VARCHAR2(20) | Primary key |
| `name` | VARCHAR2(100) | Doctor's full name |
| `specialization` | VARCHAR2(100) | Medical specialization |
| `hospital` | VARCHAR2(100) | Hospital name |
| `experience_years` | NUMBER | Years of experience |
| `consultation_fee` | NUMBER(10,2) | Fee per consultation |

All fields are **private** with public getters and setters.

---

## DAO Functions — `doctor_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_doctors_by_specialization_and_experience(specialization, min_experience, conn)` | SELECT | Fetch doctors matching specialization AND experience >= min_experience, ordered by fee ASC |
| `retrieve_doctor_by_id(doctor_id, conn)` | SELECT | Fetch single doctor by ID, returns `None` if not found |

### Key SQL — Dual Filter Query

```sql
SELECT doctor_id, name, specialization, hospital, experience_years, consultation_fee
FROM doctor
WHERE LOWER(specialization) = LOWER(:1)
  AND experience_years >= :2
ORDER BY consultation_fee ASC
```

---

## Utility Functions — `doctor_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_specialization(specialization)` | Returns `True` if specialization is in the valid list |
| `is_valid_experience(experience)` | Returns `True` if experience >= 0 |
| `display_doctor(doctor)` | Prints all doctor fields neatly |
| `get_result_count(list)` | Returns length of doctor list |
| `get_most_affordable(list)` | Returns doctor with lowest `consultation_fee` using `lambda` |
| `get_most_experienced(list)` | Returns doctor with highest `experience_years` using `lambda` |

### Valid Specializations List

```python
VALID_SPECIALIZATIONS = [
    'cardiology', 'neurology', 'orthopedics', 'dermatology',
    'pediatrics', 'gynecology', 'oncology', 'radiology',
    'psychiatry', 'general surgery'
]
```

### Lambda Usage in Util

```python
# Most affordable — lowest fee
def get_most_affordable(doctor_list):
    return min(doctor_list, key=lambda d: d.get_consultation_fee())

# Most experienced — highest years
def get_most_experienced(doctor_list):
    return max(doctor_list, key=lambda d: d.get_experience_years())
```

---

## Main Flow — `main.py`

```
Step 1 — SEARCH DOCTORS
    ├── Input   : specialization, min_experience
    ├── Validate: is_valid_specialization(), is_valid_experience()
    ├── Call    : retrieve_doctors_by_specialization_and_experience()
    └── Display : all matching doctors

Step 2 — HIGHLIGHT BEST PICKS
    ├── Call    : get_most_affordable(result)
    ├── Call    : get_most_experienced(result)
    └── Display : most affordable and most experienced doctor
```

---

## Sample Run

```
========================================
        DOCTOR SEARCH SYSTEM
========================================
Enter Specialization        : Cardiology
Enter Minimum Experience    : 10

Total Doctors Found : 3
----------------------------------------
Doctor ID        : D501
Name             : Dr. Suresh Patel
Specialization   : Cardiology
Hospital         : Apollo
Experience       : 15 years
Consultation Fee : 800.0
----------------------------------------
Doctor ID        : D502
Name             : Dr. Anitha Rao
Specialization   : Cardiology
Hospital         : Fortis
Experience       : 22 years
Consultation Fee : 1200.0
----------------------------------------
Doctor ID        : D503
Name             : Dr. Kiran Mehta
Specialization   : Cardiology
Hospital         : AIIMS
Experience       : 11 years
Consultation Fee : 600.0
----------------------------------------

========================================
Most Affordable Doctor:
  Name             : Dr. Kiran Mehta
  Consultation Fee : 600.0

Most Experienced Doctor:
  Name             : Dr. Anitha Rao
  Experience       : 22 years
========================================
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid specialization input | `"Invalid Specialization"` |
| Experience < 0 | `"Invalid Experience"` |
| No doctors found | `"No doctors found"` |
| Empty list in analytics | Returns `None` from `get_most_affordable()` / `get_most_experienced()` |

---

## Key Python Concepts Used

```python
# Two WHERE conditions with case-insensitive match
WHERE LOWER(specialization) = LOWER(:1)
  AND experience_years >= :2

# ORDER BY fee ascending — cheapest first
ORDER BY consultation_fee ASC

# lambda with min() to find most affordable
min(doctor_list, key=lambda d: d.get_consultation_fee())

# lambda with max() to find most experienced
max(doctor_list, key=lambda d: d.get_experience_years())
```
