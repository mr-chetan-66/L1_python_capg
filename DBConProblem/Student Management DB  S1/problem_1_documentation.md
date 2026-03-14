# Problem 1 — Student Topper Retrieval

## Overview

The **first and most fundamental** Python + Oracle Database connectivity problem. Covers basic **SELECT with WHERE filter and ORDER BY**, reading DB credentials from a properties file, and mapping query results to Python objects.

---

## File Structure

```
problem_1_student/
│
├── database.properties    → DB credentials config
├── student.py             → Entity class (5 fields, getters & setters)
├── student_dao.py         → DAO (1 DB function)
├── student_util.py        → Utility helpers (validation, display, count)
└── main.py                → Entry point (search and display flow)
```

---

## Oracle Table

```sql
CREATE TABLE student (
    student_id  NUMBER PRIMARY KEY,
    name        VARCHAR2(100),
    department  VARCHAR2(100),
    year        NUMBER,
    marks       NUMBER
);
```

---

## Entity Class — `student.py`

| Field | Type | Description |
|-------|------|-------------|
| `student_id` | NUMBER | Primary key |
| `name` | VARCHAR2(100) | Student's full name |
| `department` | VARCHAR2(100) | Department name |
| `year` | NUMBER | Year of study |
| `marks` | NUMBER | Marks scored |

All fields are **private** with public getters and setters.

---

## DAO Function — `student_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_toppers_by_department(department, conn)` | SELECT | Fetch all students in given department with marks >= 90, ordered by marks DESC |

### Key SQL

```sql
SELECT student_id, name, department, year, marks
FROM student
WHERE LOWER(department) = LOWER(:1)
  AND marks >= 90
ORDER BY marks DESC
```

> **Note:** `LOWER(:1)` makes the department filter **case-insensitive** — so "Computer Science", "computer science", and "COMPUTER SCIENCE" all match the same records.

---

## Utility Functions — `student_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_department(department)` | Returns `True` if department is in the valid list |
| `display_student(student)` | Prints all student fields neatly |
| `get_result_count(list)` | Returns length of student list |

### Valid Departments List

```python
VALID_DEPARTMENTS = [
    'computer science', 'electronics', 'mechanical',
    'civil', 'information technology'
]
```

---

## How DB Connection Works — `db_config.py`

```python
# Read database.properties file
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines()
             if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

# Connect using credentials
conn = cx_Oracle.connect(db['DB_USERNAME'], db['DB_PASSWORD'], db['DSN'])
```

> **Note:** Lines starting with `#` are comments and are skipped. The result is a dictionary like `{'DB_USERNAME': 'scott', 'DB_PASSWORD': 'tiger', 'DSN': 'localhost/XE'}`.

---

## How Results Are Mapped to Objects

```python
rows = cursor.fetchall()       # list of tuples from DB

for row in rows:
    student_obj = st.Student(row[0], row[1], row[2], row[3], row[4])
    student_list.append(student_obj)
```

Each `row` is a tuple — `row[0]` is the first column, `row[1]` is the second, and so on, matching the order in the SELECT statement.

---

## Main Flow — `main.py`

```
Step 1 — TAKE INPUT AND VALIDATE
    ├── Input   : department
    └── Validate: is_valid_department()

Step 2 — FETCH AND DISPLAY STUDENTS
    ├── Call    : retrieve_toppers_by_department(department, conn)
    ├── If empty: print "No toppers found" and return
    ├── Print   : total toppers found
    └── Display : each student one by one
```

---

## Sample Run

```
========================================
Enter the department: Computer Science

Total toppers found: 2
----------------------------------------
Student ID  : 101
Name        : Ananya Sharma
Year        : 3
Marks       : 97
----------------------------------------
Student ID  : 104
Name        : Ravi Kumar
Year        : 2
Marks       : 92
----------------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid department input | `"Invalid Department"` |
| No students with marks >= 90 | `"No toppers found"` |

---

## Key Python Concepts Used

```python
# Case-insensitive department match
WHERE LOWER(department) = LOWER(:1)

# Filter condition for toppers
AND marks >= 90

# Sort highest marks first
ORDER BY marks DESC

# Validate input before querying
if not util.is_valid_department(department):
    print("Invalid Department")
    return

# Map each DB row to a Student object
student_obj = st.Student(row[0], row[1], row[2], row[3], row[4])

# Return empty list if no results
if not rows:
    return []
```
