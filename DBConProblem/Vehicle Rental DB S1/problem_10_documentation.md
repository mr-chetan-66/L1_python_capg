# Problem 10 — Vehicle Rental Management System

## Overview

A full **CRUD-based** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This is the most advanced problem in the series, covering all four database operations — INSERT, SELECT, UPDATE, and DELETE — in a single cohesive system.

---

## File Structure

```
problem_10_rental/
│
├── database.properties      → DB credentials config
├── rental.py                → Entity class (8 fields, getters & setters)
├── rental_dao.py            → Class-based DAO (5 DB methods)
├── rental_util.py           → Utility helpers (validation, display, calculations)
└── main.py                  → Entry point (4-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `rental.py` | Entity class — 8 fields, getters & setters |
| `rental_dao.py` | Class-based DAO — 5 methods: retrieve by ID, INSERT with auto total, pending SELECT, UPDATE to Paid, DELETE with status guard |
| `rental_util.py` | Helpers — date/rate validation, display, rental days calc, total pending amount, longest rental, status label |
| `main.py` | Entry point — 4-step flow: create → view pending → mark paid → cancel |

---

## CRUD Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **INSERT** | `create_rental()` | Auto-calculates `total_amount = days × daily_rate` |
| **SELECT** | `retrieve_pending_rentals()` | Filters by `payment_status = 'Pending'` |
| **UPDATE** | `mark_as_paid()` | Blocks if already `'Paid'` |
| **DELETE** | `cancel_rental()` | Blocks if status is `'Paid'` — only Pending can be cancelled |

---

## New Concepts vs Problem 9

| Concept | Details |
|---------|---------|
| **Full CRUD** | First problem with all 4 DB operations in one system |
| **Auto-calculated field** | `total_amount` computed in Python before INSERT |
| **State-guarded UPDATE** | Cannot mark as Paid if already Paid |
| **State-guarded DELETE** | Cannot cancel if already Paid |
| **4-step main flow** | Create → View Pending → Mark Paid → Cancel |
| **Post-operation refresh** | Re-fetches and recalculates after each mutation |

---

## Oracle Table

```sql
CREATE TABLE rental (
    rental_id      NUMBER PRIMARY KEY,
    customer_id    NUMBER,
    vehicle_id     NUMBER,
    start_date     DATE,
    end_date       DATE,
    daily_rate     NUMBER(10,2),
    total_amount   NUMBER(10,2),
    payment_status VARCHAR2(20)
);
```

---

## Entity Class — `rental.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `rental_id` | NUMBER | Primary key |
| `customer_id` | NUMBER | ID of the customer |
| `vehicle_id` | NUMBER | ID of the rented vehicle |
| `start_date` | DATE | Rental start date |
| `end_date` | DATE | Rental end date |
| `daily_rate` | NUMBER(10,2) | Cost per day |
| `total_amount` | NUMBER(10,2) | Auto-calculated total cost |
| `payment_status` | VARCHAR2(20) | `'Pending'` or `'Paid'` |

All fields are **private** with public getters and setters following encapsulation principles.

---

## DAO Class — `rental_dao.py`

```python
class RentalDao:
    def __init__(self, conn): ...
```

### Methods

#### `retrieve_rental_by_id(rental_id)`
- Fetches a single `Rental` object by primary key
- Returns `None` if not found

#### `create_rental(rental_id, customer_id, vehicle_id, start_date, end_date, daily_rate)`
- Calculates: `num_days = (end_date - start_date).days`
- Calculates: `total_amount = num_days × daily_rate`
- Sets `payment_status = 'Pending'`
- Inserts into DB and commits
- Returns the created `Rental` object, or `None` on failure
- Wrapped in `try/except cx_Oracle.DatabaseError`

#### `retrieve_pending_rentals(customer_id)`
- Fetches all rentals for the customer where `payment_status = 'Pending'`
- Ordered by `start_date ASC`
- Returns list of `Rental` objects or empty list

#### `mark_as_paid(rental_id)`
- Returns `"Invalid Rental ID"` if not found
- Returns `"Already Paid"` if status is already `'Paid'`
- Updates `payment_status = 'Paid'` and commits
- Returns `"Payment Updated Successfully"`

#### `cancel_rental(rental_id)`
- Returns `"Invalid Rental ID"` if not found
- Returns `"Cannot Cancel Paid Rental"` if status is `'Paid'`
- Deletes the record and commits
- Returns `"Rental Cancelled Successfully"`

---

## Utility Functions — `rental_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_date_range(start, end)` | Returns `True` if `end > start` |
| `is_valid_daily_rate(rate)` | Returns `True` if `rate > 0` |
| `is_valid_rental_id(id)` | Returns `True` if `id > 0` |
| `calculate_rental_days(rental)` | Returns `(end_date - start_date).days` |
| `display_rental(rental)` | Prints all rental fields neatly |
| `get_result_count(list)` | Returns length of rental list |
| `get_total_pending_amount(list)` | Returns sum of `total_amount` across all rentals |
| `get_longest_rental(list)` | Returns rental with maximum rental days using `lambda` |
| `get_payment_status_label(rental)` | Returns `"✔ Paid"` or `"⏳ Pending"` |

---

## Main Program Flow — `main.py`

```
Step 1 — CREATE RENTAL
    ├── Input: rental_id, customer_id, vehicle_id, start_date, end_date, daily_rate
    ├── Validate: date range, daily rate
    ├── Call: rental_dao.create_rental(...)
    └── Display: created rental details

Step 2 — VIEW PENDING RENTALS
    ├── Call: rental_dao.retrieve_pending_rentals(customer_id)
    ├── Display: count, total pending amount, longest rental
    └── Display: each rental with status label

Step 3 — MARK AS PAID
    ├── Input: rental_id to mark as paid
    ├── Call: rental_dao.mark_as_paid(rental_id)
    └── Display: updated rental on success

Step 4 — CANCEL RENTAL
    ├── Input: rental_id to cancel
    ├── Call: rental_dao.cancel_rental(rental_id)
    └── Display: updated pending count and total amount
```

---

## Sample Run

```
==========================================
       VEHICLE RENTAL MANAGEMENT SYSTEM
==========================================

--- CREATE NEW RENTAL ---
Enter Rental ID      : 1001
Enter Customer ID    : 55
Enter Vehicle ID     : 301
Enter Start Date (YYYY-MM-DD) : 2024-07-01
Enter End Date   (YYYY-MM-DD) : 2024-07-05
Enter Daily Rate     : 1500

Rental Created Successfully!
Rental ID      : 1001
Customer ID    : 55
Vehicle ID     : 301
Start Date     : 2024-07-01
End Date       : 2024-07-05
Rental Days    : 4
Daily Rate     : 1500.0
Total Amount   : 6000.0
Payment Status : Pending
------------------------------------------

--- PENDING RENTALS FOR CUSTOMER 55 ---
Total Pending Rentals  : 2
Total Pending Amount   : 9500.0
Longest Rental Days    : 4
------------------------------------------
Rental ID      : 1001
Total Amount   : 6000.0
Status Label   : ⏳ Pending
------------------------------------------

--- MARK RENTAL AS PAID ---
Enter Rental ID to Mark as Paid (0 to skip) : 1001
Payment Status : Payment Updated Successfully
Updated Rental:
Rental ID      : 1001
Payment Status : Paid
------------------------------------------

--- CANCEL A RENTAL ---
Enter Rental ID to Cancel (0 to skip) : 1002
Cancellation Status : Rental Cancelled Successfully

Updated Pending Rentals Count : 0
Updated Pending Amount        : 0.0
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| `end_date <= start_date` | `"End Date Must Be After Start Date"` |
| `daily_rate <= 0` | `"Invalid Daily Rate"` |
| Invalid date format input | `"Invalid Date Format"` (caught by `ValueError`) |
| Rental ID not found | `"Invalid Rental ID"` |
| Mark paid on already paid rental | `"Already Paid"` |
| Cancel a paid rental | `"Cannot Cancel Paid Rental"` |
| DB insertion error | Returns `None` → prints `"Rental Creation Failed"` |

---

## Key Python Concepts Used

```python
# Auto-calculating total before INSERT
num_days     = (end_date - start_date).days
total_amount = round(num_days * daily_rate, 2)

# Safe date parsing with error handling
try:
    start_date = date.fromisoformat(start_str)
except ValueError:
    print("Invalid Date Format")

# Lambda for finding longest rental
max(rental_list, key=lambda r: calculate_rental_days(r))

# Handling Oracle datetime vs date safely
start = rental.get_start_date().date() \
        if hasattr(rental.get_start_date(), 'date') \
        else rental.get_start_date()

# cx_Oracle exception handling in INSERT
except cx_Oracle.DatabaseError:
    return None
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
| 6 | Doctor Search | SELECT + dual filter + lambda highlight |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Vehicle Insurance | SELECT + SYSDATE + UPDATE renewal |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| **10** | **Vehicle Rental** | **Class-based DAO + Full CRUD** |
