# Problem 7 — Subscription Service Management System

## Overview

A **SELECT + UPDATE + collections + file export** Python + Oracle Database connectivity problem
using a **class-based DAO pattern**. Covers date-range expiry logic with `relativedelta`,
4-bucket dictionary grouping, ordered multi-exception validation, and selective file export.

---

## File Structure

```
subscription_problem/
│
├── database.properties          → DB credentials config
├── subscription.py              → Entity class (8 fields, getters & setters)
├── subscription_dao.py          → Class-based DAO (4 DB methods) + 4 custom exceptions + PLAN_FEES
├── subscription_util.py         → Utility helpers (validation, expiry logic, grouping, display, export)
└── main.py                      → Entry point (4-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `subscription.py` | Entity class — 8 fields, getters & setters |
| `subscription_dao.py` | `SubscriptionDao(conn)` — 4 DB methods, 4 custom exceptions, `PLAN_FEES` constant |
| `subscription_util.py` | Helpers — validators, expiry status, days remaining, grouping, display, counts, file export |
| `main.py` | Entry point — 4-step flow: view plan → revenue → renew → export |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_subscription_by_id()` | Fetch single record by PK, return `None` if not found |
| **SELECT** | `retrieve_subscriptions_by_plan()` | Validate plan → fetch → raise exception if empty, ordered by `end_date ASC` |
| **UPDATE** | `renew_subscription()` | 3-step ordered validation → `relativedelta` → UPDATE `end_date` + commit |
| **SELECT** | `calculate_total_revenue_by_plan()` | `GROUP BY plan_type` on active subs, all 3 plans always in result |

---

## Oracle Table

```sql
CREATE TABLE subscription (
    subscription_id  NUMBER PRIMARY KEY,
    customer_name    VARCHAR2(100),
    email            VARCHAR2(100),
    plan_type        VARCHAR2(20),
    start_date       DATE,
    end_date         DATE,
    monthly_fee      NUMBER(8,2),
    is_active        NUMBER(1)    -- 1 = Active, 0 = Inactive
);
```

### Sample Records

| sub_id | customer_name | email           | plan_type | start_date | end_date   | monthly_fee | is_active |
|--------|---------------|-----------------|-----------|------------|------------|-------------|-----------|
| 1001   | Arjun Mehta   | arjun@mail.com  | Basic     | 01-01-2024 | 25-07-2024 | 199.0       | 1         |
| 1002   | Sneha Rao     | sneha@mail.com  | Basic     | 01-03-2024 | 05-08-2024 | 199.0       | 1         |
| 1003   | Kiran Das     | kiran@mail.com  | Basic     | 01-05-2024 | 01-09-2024 | 199.0       | 1         |
| 1004   | Divya Nair    | divya@mail.com  | Standard  | 01-02-2024 | 20-07-2024 | 499.0       | 1         |
| 1005   | Rahul Singh   | rahul@mail.com  | Standard  | 01-04-2024 | 15-11-2024 | 499.0       | 1         |
| 1006   | Meena Pillai  | meena@mail.com  | Premium   | 01-01-2024 | 31-12-2024 | 999.0       | 1         |
| 1007   | Suresh Iyer   | suresh@mail.com | Premium   | 01-06-2024 | 31-07-2024 | 999.0       | 0         |

---

## Entity Class — `subscription.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `subscription_id` | NUMBER | Primary key |
| `customer_name` | VARCHAR2(100) | Customer's full name |
| `email` | VARCHAR2(100) | Customer's email address |
| `plan_type` | VARCHAR2(20) | `'Basic'`, `'Standard'`, or `'Premium'` |
| `start_date` | DATE | Subscription start date |
| `end_date` | DATE | Subscription end date |
| `monthly_fee` | NUMBER(8,2) | Monthly charge for the plan |
| `is_active` | NUMBER(1) | `1` = Active, `0` = Inactive |

All fields are **private** with public getters and setters following encapsulation principles.

---

## DAO Class — `subscription_dao.py`

```python
class SubscriptionDao:
    def __init__(self, conn): ...
```

### Constants

```python
PLAN_FEES = {
    'basic'    : 199.0,
    'standard' : 499.0,
    'premium'  : 999.0
}
```

### Custom Exceptions (defined in `subscription_dao.py`)

| Exception | When Raised |
|-----------|-------------|
| `InvalidPlanTypeException` | Plan not in `PLAN_FEES` / renewal months out of range |
| `SubscriptionNotFoundException` | No records for valid plan / subscription ID not found |
| `SubscriptionAlreadyActiveException` | (reserved for future use) |
| `SubscriptionInactiveException` | Attempting to renew an inactive subscription |

### Methods

#### `retrieve_subscription_by_id(subscription_id)`
- Fetches a single `Subscription` object by primary key
- Returns `None` if not found
- Handles Oracle datetime → date safely

#### `retrieve_subscriptions_by_plan(plan_type)`
- Step 1: Validates `plan_type.lower()` against `PLAN_FEES` → raises `InvalidPlanTypeException`
- Step 2: Queries DB with `LOWER(plan_type) = :1`, ordered by `end_date ASC`
- Step 3: Raises `SubscriptionNotFoundException` if no rows returned
- Returns list of `Subscription` objects

#### `renew_subscription(subscription_id, renewal_months)`
- Step 1: Calls `retrieve_subscription_by_id()` → raises `SubscriptionNotFoundException` if `None`
- Step 2: Checks `is_active == 1` → raises `SubscriptionInactiveException` if not
- Step 3: Checks `1 <= renewal_months <= 12` → raises `InvalidPlanTypeException` if not
- Calculates: `new_end_date = end_date + relativedelta(months=renewal_months)`
- Calculates: `total_cost = round(renewal_months × monthly_fee, 2)`
- Updates `end_date` in DB, commits
- Returns tuple: `(new_end_date, total_cost)` or `None` on `DatabaseError`

#### `calculate_total_revenue_by_plan()`
- Initialises `revenue = {'Basic': 0.0, 'Standard': 0.0, 'Premium': 0.0}` first
- Runs `GROUP BY plan_type` query on `is_active = 1` records
- Uses `row[0].title()` to normalise plan name casing
- Returns revenue dict — all 3 keys always present, missing plans stay `0.0`

---

## Utility Functions — `subscription_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_subscription_id(id)` | Returns `True` if `id > 0` |
| `is_valid_renewal_months(months)` | Returns `True` if `1 <= months <= 12` |
| `get_expiry_status(end_date)` | Returns `'Expired'` / `'Expires Today'` / `'Expiring Soon'` / `'Active'` based on days remaining |
| `get_days_remaining(end_date)` | Returns `(end_date - date.today()).days` — negative if expired |
| `group_subscriptions_by_expiry_status(list)` | Returns dict of status → list, only populated keys present, using `lambda` via `get_expiry_status` |
| `get_status_label(subscription)` | Returns emoji-prefixed label: `"✔ Active"`, `"⚠ Expiring Soon"`, etc. |
| `display_subscription(subscription)` | Prints all 10 fields with aligned labels |
| `get_result_count(list)` | Returns length of list |
| `get_active_count(list)` | Returns count of subscriptions with status `'Active'` |
| `get_non_active_count(list)` | Returns count needing alerts (non-Active) |
| `export_expiry_alert_report(list, filename)` | Writes non-Active records to file with header, raises `IOError` on failure |

---

## Main Program Flow — `main.py`

```
Step 1 — VIEW SUBSCRIPTIONS BY PLAN
    ├── Input: plan_type
    ├── Call: subscription_dao.retrieve_subscriptions_by_plan(plan_type)
    ├── Catch: InvalidPlanTypeException / SubscriptionNotFoundException → print + return
    ├── Call: util.group_subscriptions_by_expiry_status(subscriptions)
    └── Display: grouped report + total count + active count + alerts count

Step 2 — MONTHLY REVENUE BY PLAN
    ├── Call: subscription_dao.calculate_total_revenue_by_plan()
    └── Display: revenue per plan (all 3 plans)

Step 3 — RENEW A SUBSCRIPTION
    ├── Input: subscription_id, renewal_months
    ├── Validate: is_valid_subscription_id
    ├── Call: subscription_dao.renew_subscription(sub_id, renewal_months)
    ├── Catch: SubscriptionNotFoundException / SubscriptionInactiveException /
    │         InvalidPlanTypeException / ValueError → print + return
    └── Display: new end date and total renewal cost

Step 4 — EXPORT EXPIRY ALERT REPORT
    ├── Input: filename
    ├── Call: util.export_expiry_alert_report(subscriptions, filename)
    └── Display: success message or IOError message
```

---

## Sample Run (today = 05-08-2024)

```
=======================================================
       SUBSCRIPTION SERVICE MANAGEMENT SYSTEM
=======================================================

--- VIEW SUBSCRIPTIONS BY PLAN ---
Enter Plan Type (Basic / Standard / Premium) : Basic

Subscription Report - Basic Plan
=======================================================

[Expired] - 1 subscription(s)
  ID       : 1001
  Customer : Arjun Mehta
  End Date : 25-07-2024
  Days     : -11
  Status   : ✗ Expired

[Expires Today] - 1 subscription(s)
  ID       : 1002
  Customer : Sneha Rao
  End Date : 05-08-2024
  Days     : 0
  Status   : ⏰ Expires Today

[Active] - 1 subscription(s)
  ID       : 1003
  Customer : Kiran Das
  End Date : 01-09-2024
  Days     : 27
  Status   : ✔ Active

Total Subscriptions : 3
Active Count        : 1
Alerts Required     : 2

--- MONTHLY REVENUE BY PLAN ---
Monthly Revenue by Plan (Active Subscriptions):
----------------------------------------
  Basic       : Rs. 597.0
  Standard    : Rs. 998.0
  Premium     : Rs. 999.0

--- RENEW A SUBSCRIPTION ---
Enter Subscription ID to Renew (0 to skip) : 1001
Enter Number of Months to Renew (1-12)     : 3
Renewal Successful!
New End Date     : 25-10-2024
Renewal Cost     : Rs. 597.0

--- EXPORT EXPIRY ALERT REPORT ---
Enter Filename to Export (e.g. alerts.txt) : alerts.txt
Expiry alert report exported to alerts.txt
```

### Exported File (`alerts.txt`)

```
SUBSCRIPTION EXPIRY ALERT REPORT
=======================================================

Subscription ID : 1001
Customer        : Arjun Mehta
Email           : arjun@mail.com
Plan            : Basic
End Date        : 25-07-2024
Status          : Expired
Days Remaining  : -11
-------------------------------------------------------
Subscription ID : 1002
Customer        : Sneha Rao
Email           : sneha@mail.com
Plan            : Basic
End Date        : 05-08-2024
Status          : Expires Today
Days Remaining  : 0
-------------------------------------------------------
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Plan type not in PLAN_FEES | `InvalidPlanTypeException` → prints message, program ends |
| Valid plan but no records in DB | `SubscriptionNotFoundException` → prints message, program ends |
| Renewal on non-existent ID | `SubscriptionNotFoundException` → prints message, program ends |
| Renewal on inactive subscription | `SubscriptionInactiveException` → prints message, program ends |
| `renewal_months` outside 1–12 | `InvalidPlanTypeException` → prints message, program ends |
| Non-numeric input for IDs/months | `ValueError` caught → prints `"Invalid input. Please enter valid values."` |
| File export failure | `IOError` caught → prints `"Export Failed: ..."` |
| No non-Active subs to export | File written with `"No subscriptions requiring alerts."` |
| DB error on UPDATE | `conn.rollback()` called → method returns `None` |

---

## Key Python Concepts Used

```python
# PLAN_FEES constant dict for plan validation
PLAN_FEES = {'basic': 199.0, 'standard': 499.0, 'premium': 999.0}
if plan_type.lower() not in PLAN_FEES:
    raise InvalidPlanTypeException(...)

# Positional bind variables (Oracle style)
cursor.execute(query, (plan_type.lower(),))

# relativedelta for month-accurate date arithmetic
from dateutil.relativedelta import relativedelta
new_end_date = current_end + relativedelta(months=renewal_months)

# GROUP BY revenue query with pre-initialised dict
revenue = {'Basic': 0.0, 'Standard': 0.0, 'Premium': 0.0}
# plan_type.title() normalises 'BASIC' → 'Basic'

# 4-bucket grouping using dict + get_expiry_status()
if status not in grouped:
    grouped[status] = []
grouped[status].append(s)

# Selective file export — skip Active, write header if nothing written
if written == 0:
    f.write("No subscriptions requiring alerts.")

# Oracle datetime vs date safety
e_date = row[5].date() if hasattr(row[5], 'date') else row[5]

# Ordered validation in renew — exists → active → months
# Each check raises a different custom exception
```

---

## Concepts Covered

| Concept | Where Used |
|---------|------------|
| DB Connectivity | Oracle SELECT with `GROUP BY`, UPDATE with commit/rollback via `db_config.py` |
| Collections | 4-bucket expiry status dict + 3-plan revenue dict, both pre-initialised |
| Date / Time Manipulation | `relativedelta` for month-accurate renewal, `days_remaining` for expiry logic |
| Custom Exceptions | 4 exceptions defined in DAO, imported and caught in `main.py` |
| File Handling | Selective export — only non-Active subs written, header always written |
| Class-based DAO | `SubscriptionDao` with `__conn`, all DB logic encapsulated |
| Encapsulation | All entity fields private, accessed only via getters/setters |

---

## Dependency

```
pip install python-dateutil
```
Required for `from dateutil.relativedelta import relativedelta` used in `renew_subscription()`.
