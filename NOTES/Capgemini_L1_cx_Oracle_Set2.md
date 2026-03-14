# 🏢 Capgemini L1 Exam — Oracle SQL with Python (cx_Oracle) | SET 2
### 20 Practice Queries | Normal → Medium | Enterprise Level

---

> **Standard Setup Used Across All Questions**
> ```python
> import cx_Oracle
> 
> conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
> cursor = conn.cursor()
> ```

> **Installing cx_Oracle**
> ```bash
> pip install cx_Oracle
> # Requires Oracle Instant Client installed on your system
> # Download from: https://www.oracle.com/database/technologies/instant-client.html
> ```

---

## 📦 Schema Reference

```sql
EMPLOYEES    (employee_id, first_name, last_name, salary, department_id, hire_date, job_id, manager_id, email, phone_number, commission_pct)
DEPARTMENTS  (department_id, department_name, location_id, manager_id)
JOBS         (job_id, job_title, min_salary, max_salary)
LOCATIONS    (location_id, city, state_province, country_id)
JOB_HISTORY  (employee_id, start_date, end_date, job_id, department_id)
COUNTRIES    (country_id, country_name, region_id)
REGIONS      (region_id, region_name)
```

---

## 🟢 NORMAL LEVEL (Q1–Q10)

---

### Q1 — Connect and Print Server Version

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

# Query Oracle data dictionary for version info
cursor.execute("SELECT * FROM v$version WHERE banner LIKE 'Oracle%'")
row = cursor.fetchone()
print(f"Oracle Server Version : {row[0]}")

# cx_Oracle client and server version from the connection object
print(f"cx_Oracle Module Version : {cx_Oracle.__version__}")
print(f"Oracle Client Version    : {cx_Oracle.clientversion()}")
print(f"Oracle DB Version        : {conn.version}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `v$version` — Oracle dynamic performance view showing full database version string.
- `cx_Oracle.__version__` — version of the installed cx_Oracle Python package.
- `cx_Oracle.clientversion()` — returns a tuple of the Oracle Instant Client version (e.g., `(21, 1, 0, 0, 0)`).
- `conn.version` — version string of the Oracle Database server the connection is attached to.
- Exam tip: cx_Oracle always requires Oracle Instant Client; `oracledb` has a Thin mode that does not.

---

### Q2 — SELECT with Multiple WHERE Conditions (AND / OR / BETWEEN)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT employee_id, first_name, last_name, salary, hire_date
    FROM employees
    WHERE (department_id = 60 OR department_id = 80)
    AND salary BETWEEN :min_sal AND :max_sal
    AND hire_date >= TO_DATE('2000-01-01', 'YYYY-MM-DD')
    ORDER BY hire_date ASC
""", min_sal=5000, max_sal=15000)

rows = cursor.fetchall()
print(f"{'ID':<6} {'Name':<22} {'Salary':>10} {'Hire Date':>12}")
print("-" * 55)
for row in rows:
    name = row[1] + ' ' + row[2]
    print(f"{row[0]:<6} {name:<22} {row[3]:>10} {str(row[4])[:10]:>12}")

print(f"\nTotal records found: {len(rows)}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- Named bind variables (`:min_sal`, `:max_sal`) passed as keyword arguments to `execute()`.
- `BETWEEN :min AND :max` — inclusive on both ends; Oracle evaluates this efficiently using index range scans.
- `TO_DATE('YYYY-MM-DD')` — converts a Python string literal into an Oracle DATE for comparison.
- Parentheses around OR conditions are critical — `AND` has higher precedence than `OR` in SQL.
- `len(rows)` — Python way to count results when already loaded into memory with `fetchall()`.

---

### Q3 — Using LIKE for Pattern Search

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

search_term = "S%"   # Last names starting with S

cursor.execute("""
    SELECT employee_id, first_name, last_name, job_id
    FROM employees
    WHERE UPPER(last_name) LIKE UPPER(:search)
    ORDER BY last_name ASC
""", search=search_term)

rows = cursor.fetchall()
print(f"Employees matching pattern '{search_term}':\n")
for row in rows:
    print(f"  [{row[0]}] {row[1]} {row[2]} — {row[3]}")

print(f"\nTotal found: {len(rows)}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `LIKE` with `%` — matches zero or more characters; `_` matches exactly one character.
- `UPPER()` on both sides ensures case-insensitive matching regardless of stored data format.
- Pattern is passed as a bind variable — never concatenate the pattern directly into the SQL string.
- Common patterns: `'A%'` starts with A, `'%son'` ends with son, `'%ar%'` contains ar, `'_a%'` second char is a.
- Exam tip: `ESCAPE` clause handles literal `%` or `_` in search strings — e.g., `LIKE '10\%' ESCAPE '\'`.

---

### Q4 — NULL Handling with NVL and IS NULL

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        employee_id,
        first_name,
        NVL(TO_CHAR(commission_pct), 'No Commission')      AS commission,
        NVL2(commission_pct, 'Has Commission',
                             'No Commission')               AS commission_status,
        salary + NVL(commission_pct * salary, 0)           AS total_compensation
    FROM employees
    ORDER BY commission_pct DESC NULLS LAST
""")

rows = cursor.fetchall()
print(f"{'ID':<6} {'Name':<15} {'Commission':<15} {'Status':<16} {'Total Comp':>12}")
print("-" * 70)
for row in rows:
    print(f"{row[0]:<6} {row[1]:<15} {str(row[2]):<15} {row[3]:<16} {row[4]:>12.2f}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `NVL(expr, default)` — substitutes a default value when expr is NULL.
- `NVL2(expr, not_null_val, null_val)` — branches on whether expr IS NULL or not.
- `NULLS LAST` in ORDER BY — pushes NULL commission rows to the bottom (Oracle default for DESC is NULLS FIRST).
- NULL arithmetic rule: `NULL * salary = NULL` — so `NVL(commission_pct * salary, 0)` is essential.
- Exam: also know `NULLIF(a, b)` — returns NULL if a equals b, else returns a; and `COALESCE(a,b,c)` — returns first non-NULL.

---

### Q5 — String Functions (CONCAT, SUBSTR, INSTR, LENGTH, TRIM)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        employee_id,
        first_name || ' ' || last_name              AS full_name,
        LENGTH(first_name || last_name)             AS name_length,
        UPPER(first_name)                           AS upper_first,
        LOWER(last_name)                            AS lower_last,
        SUBSTR(email, 1, INSTR(email, '@') - 1)    AS email_prefix,
        TRIM(first_name)                            AS trimmed_name,
        LPAD(TO_CHAR(salary), 10, '*')             AS salary_stars,
        REPLACE(job_id, '_', '-')                   AS formatted_job
    FROM employees
    WHERE department_id = 60
""")

rows = cursor.fetchall()
print(f"{'ID':<6} {'Full Name':<22} {'Len':>4} {'Email Prefix':<15} {'Job':>12}")
print("-" * 65)
for row in rows:
    print(f"{row[0]:<6} {row[1]:<22} {row[2]:>4} {str(row[5]):<15} {row[8]:>12}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `||` — Oracle string concatenation (not `+` like Python — common exam trap).
- `SUBSTR(str, start, length)` — 1-based indexing in Oracle (not 0-based like Python).
- `INSTR(str, search_str)` — returns position of first match; returns 0 if not found.
- `LPAD(str, total_width, pad_char)` — left-pads to total_width; use `RPAD` for right-padding.
- `REPLACE(str, old, new)` — replaces all occurrences (no regex; use `REGEXP_REPLACE` for patterns).
- `TRIM` removes both leading and trailing spaces; `LTRIM`/`RTRIM` for one side only.

---

### Q6 — Date Functions (SYSDATE, ADD_MONTHS, MONTHS_BETWEEN, TRUNC)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        employee_id,
        first_name,
        hire_date,
        SYSDATE                                                AS today,
        ROUND(MONTHS_BETWEEN(SYSDATE, hire_date) / 12, 1)    AS years_of_service,
        ADD_MONTHS(hire_date, 6)                              AS probation_end,
        TRUNC(hire_date, 'YEAR')                              AS hire_year_start,
        TRUNC(hire_date, 'MONTH')                             AS hire_month_start,
        LAST_DAY(hire_date)                                   AS last_day_of_hire_month,
        NEXT_DAY(hire_date, 'MONDAY')                        AS first_monday_after_hire
    FROM employees
    WHERE department_id = 90
""")

rows = cursor.fetchall()
for row in rows:
    print(f"\nEmployee : {row[1]} (ID: {row[0]})")
    print(f"  Hired             : {str(row[2])[:10]}")
    print(f"  Years of Service  : {row[4]}")
    print(f"  Probation Ends    : {str(row[5])[:10]}")
    print(f"  Hire Year Start   : {str(row[6])[:10]}")
    print(f"  Last Day of Month : {str(row[8])[:10]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `SYSDATE` — Oracle current date and time; no parentheses needed (unlike a function call).
- `MONTHS_BETWEEN(d1, d2)` — returns fractional months; divide by 12 for years.
- `ADD_MONTHS(date, n)` — adds n months; handles month-end dates correctly (e.g., Jan 31 + 1 month = Feb 28).
- `TRUNC(date, 'YEAR')` → Jan 1 of that year; `TRUNC(date, 'MONTH')` → 1st of that month.
- `LAST_DAY(date)` — last calendar day of the month containing the date.
- `NEXT_DAY(date, 'DAY_NAME')` — next occurrence of a weekday after a given date.

---

### Q7 — Aggregate Functions (SUM, AVG, MIN, MAX, COUNT)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        department_id,
        COUNT(*)                       AS total_employees,
        COUNT(commission_pct)          AS with_commission,
        SUM(salary)                    AS total_salary,
        ROUND(AVG(salary), 2)          AS avg_salary,
        MIN(salary)                    AS min_salary,
        MAX(salary)                    AS max_salary,
        MAX(salary) - MIN(salary)      AS salary_range
    FROM employees
    GROUP BY department_id
    HAVING COUNT(*) >= 3
    ORDER BY avg_salary DESC
""")

rows = cursor.fetchall()
print(f"{'Dept':>6} {'Total':>7} {'Comm':>6} {'Sum Salary':>12} "
      f"{'Avg':>10} {'Min':>8} {'Max':>8} {'Range':>8}")
print("-" * 75)
for row in rows:
    print(f"{str(row[0]):>6} {row[1]:>7} {row[2]:>6} {row[3]:>12} "
          f"{row[4]:>10} {row[5]:>8} {row[6]:>8} {row[7]:>8}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `COUNT(*)` — counts ALL rows including those with NULLs.
- `COUNT(commission_pct)` — counts only rows where commission_pct is NOT NULL.
- `HAVING` filters groups after `GROUP BY`; `WHERE` filters individual rows before grouping.
- Exam trap: aggregate functions (`SUM`, `AVG`, etc.) are NOT allowed in a `WHERE` clause.
- Salary range (`MAX - MIN`) is a common derived metric in enterprise payroll reports.
- `GROUP BY` must include all non-aggregated columns in the SELECT list.

---

### Q8 — Subquery in WHERE Clause

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT employee_id, first_name, last_name, salary, department_id
    FROM employees
    WHERE salary > (
        SELECT AVG(salary) FROM employees
    )
    AND department_id IN (
        SELECT department_id
        FROM departments
        WHERE department_name IN ('IT', 'Finance', 'Sales')
    )
    ORDER BY salary DESC
""")

rows = cursor.fetchall()
print("Employees above average salary in IT / Finance / Sales:\n")
for row in rows:
    print(f"  [{row[0]}] {row[1]} {row[2]} | ₹{row[3]:,.0f} | Dept {row[4]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- **Scalar subquery** — `salary > (SELECT AVG(...))` returns exactly ONE value; outer query compares against it.
- **List subquery** — `department_id IN (SELECT ...)` returns multiple values for an IN check.
- Inner queries execute first; their results feed the outer query's WHERE clause.
- Exam rule: scalar subquery MUST return exactly one row and one column — more rows = `ORA-01427` error.
- Alternative to IN subquery: `EXISTS` (generally faster on large tables).

---

### Q9 — CASE Expression (Simple and Searched)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        employee_id,
        first_name,
        salary,
        department_id,
        CASE department_id
            WHEN 60  THEN 'IT Department'
            WHEN 80  THEN 'Sales Department'
            WHEN 90  THEN 'Executive'
            ELSE          'Other'
        END AS dept_label,
        CASE
            WHEN salary < 5000  THEN 'Entry Level'
            WHEN salary < 10000 THEN 'Mid Level'
            WHEN salary < 20000 THEN 'Senior Level'
            ELSE                     'Executive Level'
        END AS salary_band
    FROM employees
    ORDER BY salary DESC
""")

rows = cursor.fetchall()
print(f"{'ID':<6} {'Name':<15} {'Salary':>10} {'Dept Label':<20} {'Band':<16}")
print("-" * 72)
for row in rows:
    print(f"{row[0]:<6} {row[1]:<15} {row[2]:>10} {row[4]:<20} {row[5]:<16}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- **Simple CASE**: `CASE column WHEN val THEN result END` — equality checks only.
- **Searched CASE**: `CASE WHEN condition THEN result END` — supports any boolean expression.
- CASE expressions can appear in SELECT, WHERE, ORDER BY, and GROUP BY clauses.
- `ELSE` is optional; if omitted and no condition matches, NULL is returned.
- Exam: `DECODE(col, val1, res1, val2, res2, default)` is Oracle's older equivalent — know both syntaxes.

---

### Q10 — DISTINCT and ORDER BY with Multiple Columns

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT DISTINCT
        d.department_name,
        j.job_title,
        j.min_salary,
        j.max_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    JOIN jobs j        ON e.job_id        = j.job_id
    ORDER BY d.department_name ASC, j.max_salary DESC
""")

rows = cursor.fetchall()
current_dept = None

for row in rows:
    if row[0] != current_dept:
        print(f"\n📁 {row[0]}")
        current_dept = row[0]
    print(f"   └─ {row[1]:<35} ₹{row[2]:>8} – ₹{row[3]:>8}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `DISTINCT` applies to the entire row — eliminates rows where ALL columns are identical.
- Three-table JOIN using table aliases (`e`, `d`, `j`) — cleaner and required when column names overlap.
- `ORDER BY` on multiple columns: primary sort by department name, secondary by max_salary descending.
- Python-side grouping with `current_dept` variable simulates a break-on-change display without needing GROUP BY.
- Exam: `DISTINCT` is placed immediately after SELECT and cannot be used per-column independently.

---

## 🟡 MEDIUM LEVEL (Q11–Q20)

---

### Q11 — Self JOIN (Manager–Employee Relationship)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name     AS employee_name,
        e.salary                                AS emp_salary,
        m.first_name || ' ' || m.last_name     AS manager_name,
        m.salary                                AS mgr_salary,
        ROUND((e.salary / m.salary) * 100, 1)  AS pct_of_mgr_salary
    FROM employees e
    JOIN employees m ON e.manager_id = m.employee_id
    WHERE e.department_id = 80
    ORDER BY pct_of_mgr_salary DESC
""")

rows = cursor.fetchall()
print(f"{'Employee':<25} {'Emp Sal':>10} {'Manager':<25} {'Mgr Sal':>10} {'% of Mgr':>10}")
print("-" * 85)
for row in rows:
    print(f"{row[1]:<25} {row[2]:>10} {row[3]:<25} {row[4]:>10} {str(row[5])+'%':>10}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- **Self JOIN** — the EMPLOYEES table is joined to itself using two different aliases (`e` for employee, `m` for manager).
- `e.manager_id = m.employee_id` — links each employee row to their manager's row.
- INNER JOIN excludes employees with NULL manager_id (the CEO); use `LEFT JOIN` to include root.
- `pct_of_mgr_salary` — derived metric showing each employee's pay relative to their manager.
- Classic interview pattern: self-referencing tables, org chart traversal.

---

### Q12 — OUTER JOIN (LEFT, RIGHT, FULL)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

# LEFT JOIN: All departments, including those with no employees
cursor.execute("""
    SELECT
        d.department_id,
        d.department_name,
        COUNT(e.employee_id)     AS emp_count,
        NVL(SUM(e.salary), 0)   AS total_salary
    FROM departments d
    LEFT JOIN employees e ON d.department_id = e.department_id
    GROUP BY d.department_id, d.department_name
    ORDER BY emp_count DESC
""")

rows = cursor.fetchall()
print("All Departments (including empty ones):\n")
print(f"{'Dept ID':>8} {'Department':<30} {'Headcount':>10} {'Total Salary':>14}")
print("-" * 68)
for row in rows:
    flag = "  ⚠️  EMPTY" if row[2] == 0 else ""
    print(f"{row[0]:>8} {row[1]:<30} {row[2]:>10} {row[3]:>14}{flag}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `LEFT JOIN` — returns ALL rows from the LEFT table (departments), NULLs for unmatched right side.
- `RIGHT JOIN` — opposite: all rows from the right table, NULLs on the left where no match.
- `FULL OUTER JOIN` — all rows from both sides; NULLs on both sides where no match exists.
- Oracle legacy syntax: `WHERE e.department_id(+) = d.department_id` — `(+)` on the nullable side; still seen in older codebases and exams.
- `NVL(SUM(...), 0)` — SUM of zero rows returns NULL, not 0; NVL fixes this.

---

### Q13 — ROWNUM vs ROW_NUMBER() for Top-N Queries

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

print("=== Method 1: ROWNUM (Oracle Classic — needs subquery) ===")
cursor.execute("""
    SELECT * FROM (
        SELECT employee_id, first_name, salary
        FROM employees
        ORDER BY salary DESC
    )
    WHERE ROWNUM <= 5
""")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== Method 2: ROW_NUMBER() Window Function (Pagination) ===")
cursor.execute("""
    SELECT employee_id, first_name, salary, rn
    FROM (
        SELECT employee_id, first_name, salary,
               ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
        FROM employees
    )
    WHERE rn BETWEEN 6 AND 10
""")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== Method 3: FETCH FIRST (Oracle 12c+ — Cleanest) ===")
cursor.execute("""
    SELECT employee_id, first_name, salary
    FROM employees
    ORDER BY salary DESC
    FETCH FIRST 5 ROWS ONLY
""")
for row in cursor.fetchall():
    print(f"  {row}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `ROWNUM` is assigned BEFORE ORDER BY is applied — must use a subquery to sort first, then apply ROWNUM.
- Exam trap: `SELECT ... ORDER BY salary DESC WHERE ROWNUM <= 5` gives WRONG results — ROWNUM filters before sort.
- `ROW_NUMBER() OVER (ORDER BY ...)` — window function; assigned after sorting; enables true pagination (rows 6–10).
- `FETCH FIRST N ROWS ONLY` — cleanest syntax available from Oracle 12c onwards.
- `FETCH FIRST N ROWS WITH TIES` — includes extra rows that tie for the last position.

---

### Q14 — UNION, UNION ALL, INTERSECT, MINUS

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

print("=== UNION (unique job+dept combos across current & history) ===")
cursor.execute("""
    SELECT job_id, department_id FROM employees
    UNION
    SELECT job_id, department_id FROM job_history
    ORDER BY department_id
""")
print(f"UNION row count    : {len(cursor.fetchall())}")

print("\n=== UNION ALL (with duplicates) ===")
cursor.execute("""
    SELECT job_id, department_id FROM employees
    UNION ALL
    SELECT job_id, department_id FROM job_history
""")
print(f"UNION ALL row count: {len(cursor.fetchall())}")

print("\n=== INTERSECT (job_ids in both current and history) ===")
cursor.execute("""
    SELECT job_id FROM employees
    INTERSECT
    SELECT job_id FROM job_history
""")
rows = cursor.fetchall()
print(f"Common job IDs     : {[r[0] for r in rows]}")

print("\n=== MINUS (job_ids only in current employees, not in history) ===")
cursor.execute("""
    SELECT job_id FROM employees
    MINUS
    SELECT job_id FROM job_history
""")
rows = cursor.fetchall()
print(f"Exclusive job IDs  : {[r[0] for r in rows]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `UNION` — combines result sets and removes all duplicate rows (extra sort/dedup step).
- `UNION ALL` — combines result sets and keeps duplicates; faster than UNION due to no dedup.
- `INTERSECT` — returns only rows present in BOTH result sets.
- `MINUS` — returns rows in the first set that do NOT appear in the second set (`EXCEPT` in standard SQL).
- Rule: all set operations require the same number of columns and compatible data types in each SELECT.
- Order of precedence: INTERSECT > UNION/MINUS; use parentheses to control evaluation order.

---

### Q15 — WITH Clause (Common Table Expression — CTE)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    WITH dept_stats AS (
        SELECT
            department_id,
            ROUND(AVG(salary), 2)  AS dept_avg_salary,
            COUNT(*)               AS headcount
        FROM employees
        GROUP BY department_id
    ),
    high_value_depts AS (
        SELECT department_id, dept_avg_salary, headcount
        FROM dept_stats
        WHERE dept_avg_salary > 8000
    )
    SELECT
        e.first_name,
        e.last_name,
        e.salary,
        h.dept_avg_salary,
        h.headcount,
        ROUND(e.salary - h.dept_avg_salary, 2) AS diff_from_avg
    FROM employees e
    JOIN high_value_depts h ON e.department_id = h.department_id
    ORDER BY diff_from_avg DESC
""")

rows = cursor.fetchall()
print(f"{'Name':<22} {'Salary':>10} {'Dept Avg':>10} {'Diff':>12} {'HC':>5}")
print("-" * 65)
for row in rows:
    diff_str = f"+{row[5]}" if row[5] > 0 else str(row[5])
    print(f"{row[0]+' '+row[1]:<22} {row[2]:>10} {row[3]:>10} {diff_str:>12} {row[4]:>5}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `WITH cte_name AS (SELECT ...)` — defines a named temporary result set for one SQL statement.
- Multiple CTEs are separated by commas; each can reference previously defined CTEs.
- CTEs improve readability over deeply nested subqueries — standard enterprise SQL practice.
- `diff_from_avg` reveals each employee's salary deviation from their department's average.
- Exam tip: CTEs exist only for the duration of the single statement — they are not stored objects.

---

### Q16 — Correlated Subquery

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        e.salary,
        e.department_id,
        (
            SELECT COUNT(*)
            FROM employees e2
            WHERE e2.department_id = e.department_id
            AND   e2.salary > e.salary
        ) AS employees_earning_more
    FROM employees e
    WHERE e.department_id IN (60, 80, 90)
    ORDER BY e.department_id, employees_earning_more
""")

rows = cursor.fetchall()
print(f"{'ID':<6} {'Name':<22} {'Salary':>10} {'Dept':>6} {'Earning More':>14}")
print("-" * 65)
for row in rows:
    print(f"{row[0]:<6} {row[1]+' '+row[2]:<22} {row[3]:>10} {row[4]:>6} {row[5]:>14}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- **Correlated subquery** — references columns from the outer query (`e.department_id`, `e.salary`).
- Executes once per outer row — less efficient than regular subqueries; avoid on millions of rows.
- `employees_earning_more = 0` → that employee is the highest earner in their department.
- Used for per-row comparisons, conditional counts, and existence checks that depend on outer row values.
- Exam difference: correlated subquery references outer alias; non-correlated is fully self-contained.

---

### Q17 — EXISTS and NOT EXISTS

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

print("=== Employees WHO HAVE job history (EXISTS) ===")
cursor.execute("""
    SELECT e.employee_id, e.first_name, e.last_name, e.job_id
    FROM employees e
    WHERE EXISTS (
        SELECT 1
        FROM job_history jh
        WHERE jh.employee_id = e.employee_id
    )
    ORDER BY e.employee_id
""")
rows = cursor.fetchall()
for r in rows:
    print(f"  [{r[0]}] {r[1]} {r[2]} — {r[3]}")

print(f"\n=== Employees with NO job history (NOT EXISTS) ===")
cursor.execute("""
    SELECT e.employee_id, e.first_name, e.last_name
    FROM employees e
    WHERE NOT EXISTS (
        SELECT 1
        FROM job_history jh
        WHERE jh.employee_id = e.employee_id
    )
    ORDER BY e.employee_id
""")
rows = cursor.fetchall()
print(f"Employees without history: {len(rows)}")
for r in rows[:5]:   # Show first 5 only
    print(f"  [{r[0]}] {r[1]} {r[2]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `EXISTS` — returns TRUE as soon as the subquery finds ONE matching row; stops checking (short-circuit).
- `SELECT 1` inside EXISTS — the column value is irrelevant; only row existence matters; `SELECT *` also works.
- `NOT EXISTS` — finds records with NO matching row in another table; clean alternative to `NOT IN`.
- Exam: `NOT IN` with NULL in the subquery always returns no rows — a dangerous silent bug; `NOT EXISTS` handles NULLs correctly.
- `EXISTS` is generally faster than `IN` when the subquery result set is large.

---

### Q18 — PIVOT — Rows to Columns Transformation

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT * FROM (
        SELECT
            department_id,
            TO_CHAR(hire_date, 'YYYY') AS hire_year,
            salary
        FROM employees
        WHERE TO_CHAR(hire_date, 'YYYY') IN ('2000','2001','2002','2003','2004','2005')
        AND   department_id IN (60, 80, 90)
    )
    PIVOT (
        COUNT(salary)
        FOR hire_year IN (
            '2000' AS yr_2000,
            '2001' AS yr_2001,
            '2002' AS yr_2002,
            '2003' AS yr_2003,
            '2004' AS yr_2004,
            '2005' AS yr_2005
        )
    )
    ORDER BY department_id
""")

# Dynamically extract column names from cursor.description
columns = [col[0] for col in cursor.description]
print(" | ".join(f"{c:<10}" for c in columns))
print("-" * 80)
for row in cursor.fetchall():
    print(" | ".join(f"{str(v):<10}" for v in row))

cursor.close()
conn.close()
```

**📝 Explanation:**
- `PIVOT` — Oracle operator that rotates unique row values into separate column headers.
- `FOR hire_year IN (...)` — explicitly lists which values become columns (Oracle PIVOT is not dynamic by default).
- Inner subquery feeds the PIVOT; the aggregate (`COUNT`) is applied per cell.
- `cursor.description` — list of 7-item tuples; `col[0]` gives the column name for each output column.
- Common enterprise use: headcount by dept × year, revenue by region × quarter, attendance by day × shift.
- Dynamic PIVOT (unknown column values) requires building the SQL string in Python with bind-safe column construction.

---

### Q19 — Inline View + Top-N Per Group

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT dept_name, emp_name, salary, dept_rank
    FROM (
        SELECT
            d.department_name                              AS dept_name,
            e.first_name || ' ' || e.last_name            AS emp_name,
            e.salary,
            RANK() OVER (
                PARTITION BY e.department_id
                ORDER BY e.salary DESC
            )                                              AS dept_rank
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
    ) ranked
    WHERE dept_rank <= 2
    ORDER BY dept_name, dept_rank
""")

rows = cursor.fetchall()
current_dept = None
for row in rows:
    if row[0] != current_dept:
        print(f"\n🏢 {row[0]}")
        current_dept = row[0]
    print(f"   #{row[3]}  {row[1]:<25}  ₹{row[2]:,.0f}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- **Inline view** — a subquery in the FROM clause treated as a named virtual table (`ranked`).
- `RANK() OVER (PARTITION BY dept ORDER BY salary DESC)` — assigns per-department salary rank.
- `WHERE dept_rank <= 2` in the outer query filters the top 2 per department.
- Window functions cannot appear directly in WHERE — wrapping in an inline view is the standard solution.
- Exam: this "top N per group" is one of the most frequently asked Oracle SQL patterns at L1/L2 level.
- `RANK` vs `DENSE_RANK`: if two employees tie at rank 1, RANK skips rank 2; DENSE_RANK does not.

---

### Q20 — MERGE Statement (UPSERT — Insert or Update)

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

# Incoming data: existing employees get salary updated; new ones get inserted
incoming_employees = [
    (101, 'John',  'Chen',    18000, 60),   # Exists  → UPDATE salary
    (306, 'Meera', 'Iyer',    72000, 80),   # New     → INSERT
    (107, 'Diana', 'Lorentz',  8000, 60),   # Exists  → UPDATE salary
]

try:
    for emp in incoming_employees:
        cursor.execute("""
            MERGE INTO employees tgt
            USING (SELECT :emp_id AS employee_id FROM dual) src
            ON (tgt.employee_id = src.employee_id)
            WHEN MATCHED THEN
                UPDATE SET tgt.salary = :new_sal
            WHEN NOT MATCHED THEN
                INSERT (employee_id, first_name, last_name,
                        salary, department_id, hire_date, job_id)
                VALUES (:emp_id, :fname, :lname,
                        :new_sal, :dept_id, SYSDATE, 'IT_PROG')
        """, emp_id=emp[0], new_sal=emp[3],
             fname=emp[1], lname=emp[2], dept_id=emp[4])

        print(f"  Employee {emp[0]} ({emp[1]} {emp[2]}): rowcount = {cursor.rowcount}")

    conn.commit()
    print("\n✅ All MERGE operations committed successfully.")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error [{error_obj.code}]: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `MERGE INTO target USING source ON (condition)` — Oracle's UPSERT: update if match, insert if not.
- `FROM DUAL` — Oracle's one-row dummy table; used here to supply bind variable values as a source row.
- `WHEN MATCHED THEN UPDATE` — runs when the ON condition is TRUE (row already exists).
- `WHEN NOT MATCHED THEN INSERT` — runs when no matching row is found.
- `SYSDATE` inside the INSERT sets hire_date automatically using the database clock.
- `DUAL` is a core Oracle concept — frequently tested; it is used whenever a SELECT needs no real source table.
- `cx_Oracle.DatabaseError` with `e.args` unpacking gives `error_obj.code` and `error_obj.message`.

---

## 📊 Quick Reference Summary — Set 2 (cx_Oracle)

| # | Topic | Level | Key Concept |
|---|-------|-------|-------------|
| Q1 | Server version check | 🟢 Normal | `conn.version`, `cx_Oracle.clientversion()` |
| Q2 | Multi-condition WHERE | 🟢 Normal | `BETWEEN`, `TO_DATE`, AND/OR precedence |
| Q3 | LIKE pattern search | 🟢 Normal | `%`, `_`, `UPPER()`, bind variable |
| Q4 | NULL handling | 🟢 Normal | `NVL`, `NVL2`, `NULLS LAST` |
| Q5 | String functions | 🟢 Normal | `\|\|`, `SUBSTR`, `INSTR`, `LPAD`, `REPLACE` |
| Q6 | Date functions | 🟢 Normal | `SYSDATE`, `ADD_MONTHS`, `TRUNC`, `LAST_DAY` |
| Q7 | Aggregate + HAVING | 🟢 Normal | `COUNT(*)` vs `COUNT(col)`, `HAVING` |
| Q8 | Subquery in WHERE | 🟢 Normal | Scalar subquery, IN subquery |
| Q9 | CASE expression | 🟢 Normal | Simple vs Searched CASE, DECODE |
| Q10 | DISTINCT + multi-sort | 🟢 Normal | `DISTINCT`, multi-column `ORDER BY` |
| Q11 | Self JOIN | 🟡 Medium | Same table two aliases, manager-emp |
| Q12 | OUTER JOINs | 🟡 Medium | LEFT/RIGHT/FULL, `(+)` legacy syntax |
| Q13 | ROWNUM vs ROW_NUMBER | 🟡 Medium | Top-N trap, pagination, window fn |
| Q14 | Set operations | 🟡 Medium | UNION ALL vs UNION, INTERSECT, MINUS |
| Q15 | WITH clause (CTE) | 🟡 Medium | Named CTEs, chaining, scope |
| Q16 | Correlated subquery | 🟡 Medium | Per-row execution, outer reference |
| Q17 | EXISTS / NOT EXISTS | 🟡 Medium | Short-circuit, NULL safety vs NOT IN |
| Q18 | PIVOT | 🟡 Medium | Row-to-column, `cursor.description` |
| Q19 | Inline view + Ranking | 🟡 Medium | Top-N per group, RANK, PARTITION BY |
| Q20 | MERGE (UPSERT) | 🟡 Medium | DUAL, WHEN MATCHED / NOT MATCHED |

---

## ⚡ cx_Oracle Key Cheat Sheet

| Task | cx_Oracle Code |
|------|---------------|
| Connect | `cx_Oracle.connect("user", "pwd", "host:port/svc")` |
| Create pool | `cx_Oracle.SessionPool(user, pwd, dsn, min, max, increment)` |
| Acquire from pool | `conn = pool.acquire()` |
| Release to pool | `pool.release(conn)` |
| Named bind | `cursor.execute("... :name", name=value)` |
| Positional bind | `cursor.execute("... :1 :2", (val1, val2))` |
| Dict bind | `cursor.execute("... :k", {"k": val})` |
| OUT variable | `v = cursor.var(cx_Oracle.NUMBER)` then `v.getvalue()` |
| Array OUT | `v = cursor.arrayvar(cx_Oracle.NUMBER, 100)` |
| Call procedure | `cursor.callproc("proc", [in1, out_var])` |
| Call function | `cursor.callfunc("func", cx_Oracle.NUMBER, [arg])` |
| REF cursor | Pass `conn.cursor()` as OUT arg in `callproc` |
| Fetch one | `cursor.fetchone()` → tuple or None |
| Fetch N | `cursor.fetchmany(n)` |
| Fetch all | `cursor.fetchall()` |
| Column names | `[col[0] for col in cursor.description]` |
| Rows affected | `cursor.rowcount` |
| Error code | `error_obj, = e.args; error_obj.code` |
| Error message | `error_obj, = e.args; error_obj.message` |
| Commit | `conn.commit()` |
| Rollback | `conn.rollback()` |
| Savepoint | `cursor.execute("SAVEPOINT sp1")` |
| Rollback to SP | `cursor.execute("ROLLBACK TO SAVEPOINT sp1")` |

---

## 🧠 Must-Know Oracle SQL Facts for Exam

| Concept | Oracle Syntax | Trap to Avoid |
|---------|--------------|---------------|
| Concatenation | `\|\|` | Never use `+` for strings in Oracle |
| Top-N | `FETCH FIRST N ROWS ONLY` | `ROWNUM` needs a subquery wrapper |
| NULL check | `IS NULL` / `IS NOT NULL` | `= NULL` always returns FALSE |
| Current timestamp | `SYSDATE` | No parentheses needed |
| Auto-increment | `sequence_name.NEXTVAL` | No AUTO_INCREMENT in Oracle |
| Dummy source | `FROM DUAL` | Required for SELECT without a table |
| UPSERT | `MERGE INTO` | Only available in Oracle SQL |
| String position | 1-based (SUBSTR) | Oracle starts at 1, Python at 0 |
| Pagination | `ROW_NUMBER()` in subquery | Cannot filter window fn in same WHERE |
| Group filter | `HAVING` | `WHERE` cannot contain aggregates |
| NOT IN + NULL | Use `NOT EXISTS` | `NOT IN` returns no rows if NULL in list |

---

*Set 2 (cx_Oracle Edition) — Capgemini L1 Oracle + Python DB Connectivity Exam*
*Normal & Medium | String/Date/NULL Functions, JOINs, Subqueries, CTEs, Set Ops, PIVOT, MERGE*
