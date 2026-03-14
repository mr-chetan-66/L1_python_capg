# Problem 9 — Exam Result Management System

## Overview

A Python + Oracle Database problem using a **class-based DAO pattern**.
Covers SELECT, DELETE, and a **subquery** — plus Python-side analytics like percentage calculation and pass/fail summary.

---

## File Structure

```
problem_9_exam/
│
├── database.properties    → DB credentials config
├── exam_result.py         → Entity class (7 fields, getters & setters)
├── exam_dao.py            → Class-based DAO (4 DB methods)
├── exam_util.py           → Utility helpers (validation, display, calculations)
└── main.py                → Entry point (3-step user flow)
```

---

## Oracle Table

```sql
CREATE TABLE exam_result (
    result_id      NUMBER PRIMARY KEY,
    student_id     NUMBER,
    subject        VARCHAR2(100),
    exam_date      DATE,
    marks_obtained NUMBER,
    max_marks      NUMBER,
    grade          VARCHAR2(5)
);
```

---

## Entity Class — `exam_result.py`

| Field | Type | Description |
|-------|------|-------------|
| `result_id` | NUMBER | Primary key |
| `student_id` | NUMBER | ID of the student |
| `subject` | VARCHAR2(100) | Subject name |
| `exam_date` | DATE | Date of exam |
| `marks_obtained` | NUMBER | Marks scored |
| `max_marks` | NUMBER | Total marks possible |
| `grade` | VARCHAR2(5) | Grade awarded (O, A+, A, B+, B, C, F) |

All fields are **private** with public getters and setters.

---

## DAO Class — `exam_dao.py`

```python
class ExamDao:
    def __init__(self, conn): ...
```

### Methods

| Method | Operation | Description |
|--------|-----------|-------------|
| `retrieve_results_by_student(student_id)` | SELECT | All results for a student, ordered by `exam_date DESC` |
| `retrieve_result_by_id(result_id)` | SELECT | Single result by primary key, returns `None` if not found |
| `delete_result(result_id)` | DELETE | Checks existence first, then deletes and commits |
| `retrieve_best_result(student_id)` | SELECT + Subquery | Finds result with highest marks using `MAX()` subquery |

### Delete Logic

```python
def delete_result(self, result_id):
    result = self.retrieve_result_by_id(result_id)   # check exists
    if result is None:
        return "Result Not Found"
    # DELETE and commit
    return "Result Deleted Successfully"
```

### Subquery Example

```sql
SELECT * FROM exam_result
WHERE student_id = :1
  AND marks_obtained = (
        SELECT MAX(marks_obtained)
        FROM exam_result
        WHERE student_id = :2
      )
```

---

## Utility Functions — `exam_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_student_id(id)` | Returns `True` if `id > 0` |
| `is_valid_result_id(id)` | Returns `True` if `id > 0` |
| `display_result(result)` | Prints all fields of one result neatly |
| `get_result_count(list)` | Returns length of results list |
| `calculate_percentage(list)` | `(sum of marks_obtained / sum of max_marks) × 100`, rounded to 2 decimal places. Returns `-1` if list is empty |
| `get_pass_fail_summary(list)` | Returns `{'passed': N, 'failed': N}` — failed if grade is `'F'` |
| `get_performance_remark(percentage)` | Returns remark string based on percentage range |

### Performance Remark Logic

| Percentage | Remark |
|------------|--------|
| >= 90 | Outstanding |
| >= 75 | Distinction |
| >= 60 | First Class |
| >= 50 | Second Class |
| >= 35 | Pass |
| < 35 | Fail |

---

## Main Flow — `main.py`

```
Step 1 — VIEW ALL RESULTS
    ├── Input  : student_id
    ├── Validate: student_id > 0
    ├── Call   : exam_dao.retrieve_results_by_student(student_id)
    └── Display: all results one by one

Step 2 — ANALYTICS SUMMARY
    ├── calculate_percentage(results)
    ├── get_performance_remark(percentage)
    ├── get_pass_fail_summary(results)
    └── retrieve_best_result(student_id)  ← uses subquery

Step 3 — DELETE A RESULT
    ├── Input  : result_id (0 to skip)
    ├── Call   : exam_dao.delete_result(result_id)
    └── Display: updated count and recalculated percentage
```

---

## Sample Run

```
========================================
       EXAM RESULT MANAGEMENT SYSTEM
========================================
Enter Student ID : 301

Total Results Found : 4
----------------------------------------
Result ID      : 9015
Student ID     : 301
Subject        : Mathematics
Exam Date      : 2024-03-10
Marks Obtained : 88 / 100
Grade          : A
----------------------------------------
Result ID      : 9014
Subject        : Physics
Marks Obtained : 74 / 100
Grade          : B+
----------------------------------------

========================================
Overall Percentage : 82.33 %
Performance Remark : Distinction
Subjects Passed    : 3
Subjects Failed    : 1
========================================

Best Performing Subject:
  Subject        : Mathematics
  Marks Obtained : 88 / 100
  Grade          : A
========================================

Enter Result ID to Delete (0 to skip) : 9012
Status : Result Deleted Successfully

Updated Total Results : 3
Updated Percentage    : 79.67 %
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Student ID <= 0 | `"Invalid Student ID"` |
| No results found | `"No Results Found"` |
| Result ID not in DB | `"Result Not Found"` |
| Empty list passed to percentage | Returns `-1` |

---

## Key Python Concepts Used

```python
# Class-based DAO — connection stored as instance variable
class ExamDao:
    def __init__(self, conn):
        self.__conn = conn

# Percentage calculation using sum + list comprehension
total_obtained = sum(r.get_marks_obtained() for r in result_list)
total_max      = sum(r.get_max_marks()      for r in result_list)
percentage     = round((total_obtained / total_max) * 100, 2)

# Pass/fail count using sum + condition
passed = sum(1 for r in result_list if r.get_grade() != 'F')
failed = sum(1 for r in result_list if r.get_grade() == 'F')

# Subquery to find best result directly in SQL
AND marks_obtained = (SELECT MAX(marks_obtained) FROM exam_result WHERE student_id = :2)
```
