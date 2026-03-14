# Problem 2 — Employee Payroll Management System

## Overview

A **single-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers SELECT with case-insensitive WHERE + ORDER BY, salary component calculation using a dictionary, complete years of experience with anniversary adjustment, and formatted payroll report file writing.

---

## File Structure

```
problem_2_payroll/
│
├── database.properties      → DB credentials config
├── employee.py              → Entity class (6 fields, getters & setters)
├── exceptions.py            → 2 custom exception classes
├── employee_dao.py          → Class-based DAO (1 DB method)
├── payroll_util.py          → Utility helpers (salary calc, experience, display, file export)
└── main.py                  → Entry point (2-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `employee.py` | Entity class — 6 fields, getters & setters |
| `exceptions.py` | 2 custom exceptions isolated in one place |
| `employee_dao.py` | Class-based DAO — 1 method: SELECT employees by department |
| `payroll_util.py` | Helpers — net salary dict, years of experience, console display, file report export |
| `main.py` | Entry point — 2-step flow: retrieve + display → export report |

---

## Database Operation Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_employees_by_department()` | Case-insensitive `LOWER()` match; sorted `ASC` by `emp_id`; raises `InvalidDepartmentException` if empty |

---

## Oracle Table

```sql
CREATE TABLE employee (
    emp_id        NUMBER PRIMARY KEY,
    emp_name      VARCHAR2(100),
    department    VARCHAR2(100),
    designation   VARCHAR2(100),
    basic_salary  NUMBER(10, 2),
    joining_date  DATE
);
```

---

## Entity Class — `employee.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `emp_id` | NUMBER | Primary key |
| `emp_name` | VARCHAR2(100) | Full name of the employee |
| `department` | VARCHAR2(100) | Department name |
| `designation` | VARCHAR2(100) | Job title |
| `basic_salary` | NUMBER(10,2) | Monthly basic salary |
| `joining_date` | DATE | Date of joining the company |

All fields are **private** with public getters and setters following encapsulation principles.

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `InvalidDepartmentException` | No employees found for the given department |
| `InsufficientExperienceException` | Employee has less than 1 complete year of experience |

---

## DAO Class — `employee_dao.py`

```python
class EmployeeDao:
    def __init__(self, conn): ...
```

### Methods

#### `retrieve_employees_by_department(department)`
- Executes `WHERE LOWER(department) = :1` using `department.lower()` for case-insensitive match
- Sorted by `emp_id ASC`
- Safely converts Oracle datetime to `date` using `hasattr(..., 'date')`
- Raises `InvalidDepartmentException` if no records found
- Returns list of `Employee` objects

---

## Utility Functions — `payroll_util.py`

| Function | Description |
|----------|-------------|
| `calculate_net_salary(basic_salary)` | Returns a dict of all salary components rounded to 2 dp |
| `calculate_years_of_experience(joining_date)` | Returns int of complete years; raises `InsufficientExperienceException` if < 1 year |
| `display_payroll(department, employee_list)` | Prints full payroll breakdown per employee to console |
| `export_payroll_report(employee_list, filename)` | Writes formatted report to file; raises `IOError` on write failure |

### Salary Calculation Rules

**Allowances (added to basic):**

| Component | Rate |
|-----------|------|
| HRA | 20% of basic_salary |
| DA | 15% of basic_salary |
| TA | 10% of basic_salary |

**Deductions (subtracted from gross):**

| Component | Rate |
|-----------|------|
| PF | 12% of basic_salary |
| Tax | 10% of basic_salary **only if** `basic_salary > 30000`; otherwise `0.0` |

**Formulas:**
```
gross_salary = basic_salary + HRA + DA + TA
net_salary   = gross_salary - PF - Tax
```

### Years of Experience Logic

```python
years = today.year - joining_date.year
# Subtract 1 if anniversary hasn't occurred yet this year
if (today.month, today.day) < (joining_date.month, joining_date.day):
    years -= 1
```

---

## Main Program Flow — `main.py`

```
Step 1 — EMPLOYEE PAYROLL DETAILS
    ├── Input: department
    ├── Call: employee_dao.retrieve_employees_by_department(department)
    ├── Call: util.display_payroll(department, employee_list)
    └── Display: full salary breakdown per employee

Step 2 — EXPORT PAYROLL REPORT
    ├── Input: filename
    ├── Call: util.export_payroll_report(employee_list, filename)
    └── Display: confirmation message
```

---

## Sample Run

```
=============================================
      EMPLOYEE PAYROLL MANAGEMENT SYSTEM
=============================================

--- EMPLOYEE PAYROLL DETAILS ---
Enter Department : IT

Employee Payroll Details - IT
=============================================
Emp ID     : 101
Name       : Arjun Mehta
Designation: Software Engineer
Basic      : 45000.0
HRA        : 9000.0
DA         : 6750.0
TA         : 4500.0
Gross      : 65250.0
PF         : 5400.0
Tax        : 4500.0
Net Salary : 55350.0
Experience : 5 year(s)
---------------------------------------------

--- EXPORT PAYROLL REPORT ---
Enter Filename to Export Report : it_payroll.txt
Payroll report exported successfully to it_payroll.txt
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Department has no employees | `InvalidDepartmentException` — "No employees found in the given department." |
| Employee joined less than 1 year ago | `InsufficientExperienceException` — "Employee has less than 1 year of experience." (printed inline per employee, does NOT stop the loop) |
| basic_salary <= 30000 | `tax = 0.0` — no tax deduction applied |
| Report file write fails | `IOError` raised from `export_payroll_report` |
| Invalid user input | `ValueError` caught in `main()` |

---

## Key Python Concepts Used

```python
# Case-insensitive department search
WHERE LOWER(department) = :1
cursor.execute(query, (department.lower(),))

# Salary dict with all components rounded to 2 dp
hra = round(basic_salary * 0.20, 2)
tax = round(basic_salary * 0.10, 2) if basic_salary > 30000 else 0.0
gross_salary = round(basic_salary + hra + da + ta, 2)
net_salary   = round(gross_salary - pf - tax, 2)

# Complete years with anniversary check
years = today.year - joining_date.year
if (today.month, today.day) < (joining_date.month, joining_date.day):
    years -= 1

# InsufficientExperienceException handled inline per employee
# so it does not break the loop — experience shown as message
try:
    exp = calculate_years_of_experience(e.get_joining_date())
    exp_display = f"{exp} year(s)"
except InsufficientExperienceException as ex:
    exp_display = str(ex)
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| **2** | **Employee Payroll** | **SELECT + salary dict + experience calc + file report** |
| 3 | Product Low Stock | SELECT + multi-condition + SYSDATE |
| 4 | Order Placement | INSERT + SELECT |
| 5 | Bank Account Transaction | SELECT + conditional UPDATE |
| 6 | Crime Record Management | Two-table DAO + Custom Exceptions + Dict Grouping + File Report |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
