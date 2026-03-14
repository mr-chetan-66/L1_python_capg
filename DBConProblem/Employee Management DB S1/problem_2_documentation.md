# Problem 2 — Employee Salary Range Search

## Overview

A Python + Oracle Database problem focused on **BETWEEN for numeric range filtering** and **Python-side aggregation** to calculate the average salary from the result list.

---

## File Structure

```
problem_2_employee/
│
├── database.properties    → DB credentials config
├── employee.py            → Entity class (6 fields, getters & setters)
├── employee_dao.py        → DAO (1 DB function)
├── employee_util.py       → Utility helpers (validation, display, average salary)
└── main.py                → Entry point (search and display flow)
```

---

## Oracle Table

```sql
CREATE TABLE employee (
    emp_id       VARCHAR2(20) PRIMARY KEY,
    name         VARCHAR2(100),
    designation  VARCHAR2(100),
    department   VARCHAR2(100),
    salary       NUMBER(10,2),
    joining_date DATE
);
```

---

## Entity Class — `employee.py`

| Field | Type | Description |
|-------|------|-------------|
| `emp_id` | VARCHAR2(20) | Primary key |
| `name` | VARCHAR2(100) | Employee's full name |
| `designation` | VARCHAR2(100) | Job title |
| `department` | VARCHAR2(100) | Department name |
| `salary` | NUMBER(10,2) | Monthly salary |
| `joining_date` | DATE | Date of joining |

All fields are **private** with public getters and setters.

---

## DAO Function — `employee_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_employees_by_salary_range(min_salary, max_salary, conn)` | SELECT | Fetch all employees with salary between min and max (inclusive), ordered by salary ASC |

### Key SQL — BETWEEN Filter

```sql
SELECT emp_id, name, designation, department, salary, joining_date
FROM employee
WHERE salary BETWEEN :1 AND :2
ORDER BY salary ASC
```

> **Note:** `BETWEEN :1 AND :2` is **inclusive** on both ends — it includes employees whose salary equals exactly `min_salary` or `max_salary`.

---

## Utility Functions — `employee_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_salary_range(min_salary, max_salary)` | Returns `True` only if both > 0 and min < max |
| `display_employee(employee)` | Prints all employee fields neatly |
| `get_result_count(list)` | Returns length of employee list |
| `calculate_average_salary(list)` | Returns average salary rounded to 2 decimal places, returns `0` if list is empty |

### Salary Range Validation Logic

```python
def is_valid_salary_range(min_salary, max_salary):
    if min_salary <= 0 or max_salary <= 0:
        return False
    if min_salary >= max_salary:
        return False
    return True
```

### Average Salary Calculation

```python
def calculate_average_salary(employee_list):
    if not employee_list:
        return 0
    total = sum(e.get_salary() for e in employee_list)
    return round(total / len(employee_list), 2)
```

---

## Main Flow — `main.py`

```
Step 1 — TAKE INPUTS AND VALIDATE
    ├── Input   : min_salary, max_salary
    └── Validate: is_valid_salary_range()

Step 2 — FETCH AND DISPLAY EMPLOYEES
    ├── Call    : retrieve_employees_by_salary_range(min_salary, max_salary, conn)
    ├── If empty: print "No employees found" and return
    ├── Print   : total employees found
    ├── Print   : average salary
    └── Display : each employee one by one
```

---

## Sample Run

```
===================================
Enter the minimum salary: 30000
Enter the maximum salary: 70000

Total employees found: 3
Average Salary       : 48333.33
-----------------------------------
Emp ID      : E201
Name        : Kiran Mehta
Designation : Junior Developer
Department  : IT
Salary      : 35000.0
Joining Date: 2021-06-15
-----------------------------------
Emp ID      : E205
Name        : Sneha Rao
Designation : Business Analyst
Department  : Finance
Salary      : 55000.0
Joining Date: 2020-03-10
-----------------------------------
Emp ID      : E210
Name        : Arjun Singh
Designation : Senior Developer
Department  : IT
Salary      : 65000.0
Joining Date: 2019-08-01
-----------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Either salary <= 0 | `"Invalid Salary Range"` |
| min_salary >= max_salary | `"Invalid Salary Range"` |
| No employees found in range | `"No employees found"` |
| Empty list in average calc | Returns `0` |

---

## Key Python Concepts Used

```python
# BETWEEN for inclusive numeric range
WHERE salary BETWEEN :1 AND :2

# ORDER BY salary ascending — lowest first
ORDER BY salary ASC

# Validate both bounds before querying
if min_salary <= 0 or max_salary <= 0:
    return False
if min_salary >= max_salary:
    return False

# Average using sum + len — Python side aggregation
total = sum(e.get_salary() for e in employee_list)
average = round(total / len(employee_list), 2)
```
