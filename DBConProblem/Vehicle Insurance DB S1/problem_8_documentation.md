# Problem 8 — Vehicle Insurance Management System

## Overview

A Python + Oracle Database problem focused on **date-based filtering using SYSDATE**, **UPDATE for insurance renewal**, and **Python-side date arithmetic** to calculate days overdue.

---

## File Structure

```
problem_8_vehicle/
│
├── database.properties    → DB credentials config
├── vehicle.py             → Entity class (7 fields, getters & setters)
├── vehicle_dao.py         → DAO (3 DB functions)
├── vehicle_util.py        → Utility helpers (validation, display, date calculations)
└── main.py                → Entry point (2-step user flow)
```

---

## Oracle Table

```sql
CREATE TABLE vehicle (
    vehicle_id        VARCHAR2(20) PRIMARY KEY,
    owner_name        VARCHAR2(100),
    vehicle_type      VARCHAR2(20),
    brand             VARCHAR2(50),
    model             VARCHAR2(50),
    registration_year NUMBER,
    insurance_expiry  DATE
);
```

---

## Entity Class — `vehicle.py`

| Field | Type | Description |
|-------|------|-------------|
| `vehicle_id` | VARCHAR2(20) | Primary key |
| `owner_name` | VARCHAR2(100) | Vehicle owner's name |
| `vehicle_type` | VARCHAR2(20) | car / bike / truck / bus |
| `brand` | VARCHAR2(50) | Vehicle brand |
| `model` | VARCHAR2(50) | Vehicle model |
| `registration_year` | NUMBER | Year of registration |
| `insurance_expiry` | DATE | Insurance expiry date |

All fields are **private** with public getters and setters.

---

## DAO Functions — `vehicle_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_vehicle_by_id(vehicle_id, conn)` | SELECT | Fetch single vehicle by ID, returns `None` if not found |
| `retrieve_expired_insurance_vehicles(vehicle_type, conn)` | SELECT + SYSDATE | Fetch all vehicles of given type where `insurance_expiry < SYSDATE`, ordered by expiry ASC |
| `renew_insurance(vehicle_id, new_expiry_date, conn)` | UPDATE | Checks existence first, then updates `insurance_expiry` and commits |

### Key SQL — Expired Insurance Filter

```sql
SELECT * FROM vehicle
WHERE LOWER(vehicle_type) = LOWER(:1)
  AND insurance_expiry < SYSDATE
ORDER BY insurance_expiry ASC
```

### Renewal Logic

```python
def renew_insurance(vehicle_id, new_expiry_date, conn):
    vehicle = retrieve_vehicle_by_id(vehicle_id, conn)  # check exists
    if vehicle is None:
        return "Invalid Vehicle ID"
    # UPDATE insurance_expiry and commit
    return "Insurance Renewed Successfully"
```

---

## Utility Functions — `vehicle_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_vehicle_type(type)` | Returns `True` if type is car / bike / truck / bus |
| `is_valid_renewal_date(date)` | Returns `True` only if date is in the future (after today) |
| `get_days_overdue(vehicle)` | Returns `(today - insurance_expiry).days` |
| `get_insurance_status(vehicle)` | Returns `"Expired"` or `"Valid"` based on expiry vs today |
| `display_vehicle(vehicle)` | Prints all vehicle fields with insurance status |
| `get_result_count(list)` | Returns length of vehicle list |
| `get_most_overdue(list)` | Returns vehicle with highest days overdue using `lambda` |

### Date Handling Note

Oracle returns `DATE` fields as Python `datetime` objects. Always extract `.date()` safely:

```python
expiry = vehicle.get_insurance_expiry().date() \
         if hasattr(vehicle.get_insurance_expiry(), 'date') \
         else vehicle.get_insurance_expiry()

days_overdue = (date.today() - expiry).days
```

---

## Main Flow — `main.py`

```
Step 1 — VIEW EXPIRED INSURANCE VEHICLES
    ├── Input   : vehicle_type (car / bike / truck / bus)
    ├── Validate: is_valid_vehicle_type()
    ├── Call    : retrieve_expired_insurance_vehicles(vehicle_type, conn)
    ├── Display : each vehicle with days overdue
    └── Highlight: most overdue vehicle

Step 2 — RENEW INSURANCE
    ├── Input   : vehicle_id, new_expiry_date (YYYY-MM-DD)
    ├── Validate: is_valid_renewal_date() — must be future date
    ├── Call    : renew_insurance(vehicle_id, new_expiry_date, conn)
    └── Display : updated vehicle details on success
```

---

## Sample Run

```
==========================================
    VEHICLE INSURANCE MANAGEMENT SYSTEM
==========================================
Enter Vehicle Type (car/bike/truck/bus): car

Total Expired Insurance Vehicles : 2
------------------------------------------
Vehicle ID         : V801
Owner Name         : Ramesh Iyer
Vehicle Type       : car
Brand              : Maruti
Model              : Swift
Registration Year  : 2018
Insurance Expiry   : 2024-02-10
Insurance Status   : Expired
------------------------------------------
Days Overdue       : 151
------------------------------------------
Vehicle ID         : V802
Owner Name         : Priya Nair
Insurance Expiry   : 2024-01-05
Days Overdue       : 187
------------------------------------------

==========================================
Most Overdue Vehicle:
  Vehicle ID   : V802
  Owner        : Priya Nair
  Days Overdue : 187
==========================================

Enter Vehicle ID to Renew Insurance  : V801
Enter New Expiry Date (YYYY-MM-DD)   : 2025-07-10

Status : Insurance Renewed Successfully

Updated Vehicle Details:
Vehicle ID         : V801
Insurance Expiry   : 2025-07-10
Insurance Status   : Valid
------------------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid vehicle type input | `"Invalid Vehicle Type"` |
| No expired vehicles found | `"No vehicles with expired insurance found"` |
| Vehicle ID not in DB | `"Invalid Vehicle ID"` |
| New expiry date is today or past | `"Renewal Date Must Be In The Future"` |
| Bad date format entered | `"Invalid Date Format"` (caught by `ValueError`) |

---

## Key Python Concepts Used

```python
# Parse date input safely
try:
    new_expiry_date = date.fromisoformat(new_expiry_str)
except ValueError:
    print("Invalid Date Format")

# Validate renewal date is in the future
def is_valid_renewal_date(new_expiry_date):
    return new_expiry_date > date.today()

# Days overdue calculation
days_overdue = (date.today() - expiry).days

# Find most overdue vehicle using lambda
most_overdue = max(vehicle_list, key=lambda v: get_days_overdue(v))
```
