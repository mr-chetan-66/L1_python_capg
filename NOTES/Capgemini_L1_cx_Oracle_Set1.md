# 🏢 Capgemini L1 Exam — Oracle SQL with Python (cx_Oracle) | SET 1
### 20 Practice Queries | Normal → Hard | Enterprise Level

---

> **Standard Setup Used Across All Questions**
> ```python
> import cx_Oracle
> 
> conn = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
> cursor = conn.cursor()
> ```

> **Installing cx_Oracle**
> ```bash
> pip install cx_Oracle
> # Also requires Oracle Instant Client installed on your machine
> ```

---

## 📦 Schema Reference (Enterprise HR Database)

```sql
EMPLOYEES    (employee_id, first_name, last_name, salary, department_id, hire_date, job_id, manager_id)
DEPARTMENTS  (department_id, department_name, location_id, manager_id)
JOBS         (job_id, job_title, min_salary, max_salary)
LOCATIONS    (location_id, city, state_province, country_id)
JOB_HISTORY  (employee_id, start_date, end_date, job_id, department_id)
```

---

## 🟢 NORMAL LEVEL (Q1–Q7)

---

### Q1 — Fetch All Employees in a Department Using Bind Variable

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

dept_id = 50

cursor.execute("""
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE department_id = :dept_id
    ORDER BY salary DESC
""", dept_id=dept_id)

rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Salary: {row[3]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `cx_Oracle.connect("user", "password", "host:port/service")` — standard connection string format.
- Named bind variable (`:dept_id`) — prevents SQL injection and enables Oracle cursor sharing for performance.
- `fetchall()` returns all matching rows as a list of tuples.
- Always close cursor and connection to free Oracle server resources.
- In cx_Oracle, bind variables can be passed as keyword arguments or a dictionary.

---

### Q2 — Insert a New Employee with Error Handling

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO employees
            (employee_id, first_name, last_name, salary, department_id, hire_date, job_id)
        VALUES
            (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7)
    """, (300, 'Rahul', 'Sharma', 75000, 60, '2024-01-15', 'IT_PROG'))

    conn.commit()
    print("Employee inserted successfully.")

except cx_Oracle.IntegrityError as e:
    error_obj, = e.args
    print(f"Integrity Error [{error_obj.code}]: {error_obj.message}")
    conn.rollback()

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Database Error [{error_obj.code}]: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- Positional bind variables (`:1, :2, ...`) — tuple values map by position.
- `cx_Oracle.IntegrityError` — raised for constraint violations (duplicate PK, FK mismatch).
- `e.args` unpacking gives access to `error_obj.code` (ORA-XXXXX) and `error_obj.message`.
- `conn.rollback()` undoes all uncommitted changes on failure.
- `finally` guarantees cleanup regardless of success or failure.

---

### Q3 — Update Salary Based on Condition

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    cursor.execute("""
        UPDATE employees
        SET salary = salary * 1.10
        WHERE department_id = :dept
        AND salary < :threshold
    """, dept=90, threshold=20000)

    print(f"Rows updated: {cursor.rowcount}")
    conn.commit()

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.rowcount` — number of rows affected by the last DML statement; key exam topic.
- Conditional UPDATE with two named bind variables in one execute call.
- 10% salary hike applied only to qualifying rows in one SQL round-trip.
- Always pair UPDATE with explicit `commit()` or `rollback()` — no auto-commit in cx_Oracle.

---

### Q4 — Delete Records and Confirm with rowcount

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    emp_id_to_delete = 300

    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id = :emp_id
    """, emp_id=emp_id_to_delete)

    if cursor.rowcount == 0:
        print("No employee found with that ID.")
    else:
        print(f"{cursor.rowcount} employee(s) deleted.")

    conn.commit()

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.rowcount == 0` confirms whether the target row actually existed before deletion.
- Safe DELETE using bind variable — never use f-strings to inject values into SQL.
- Common exam trap: forgetting `conn.commit()` after DELETE means data is NOT actually removed.
- cx_Oracle does NOT auto-commit; every DML needs an explicit `commit()`.

---

### Q5 — Fetch One Row with fetchone()

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

emp_id = 101

cursor.execute("""
    SELECT e.first_name, e.last_name, d.department_name, e.salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE e.employee_id = :emp_id
""", emp_id=emp_id)

row = cursor.fetchone()

if row:
    print(f"Name       : {row[0]} {row[1]}")
    print(f"Department : {row[2]}")
    print(f"Salary     : {row[3]}")
else:
    print("Employee not found.")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `fetchone()` returns a single tuple or `None` if no rows matched.
- `if row:` — checks for None without raising an error; always do this after fetchone().
- INNER JOIN between EMPLOYEES and DEPARTMENTS — only returns rows with a matching department.
- Efficient for lookups where exactly one row is expected (PK-based queries).

---

### Q6 — Batch Insert Using executemany()

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

employees_data = [
    (301, 'Anita', 'Verma',  60000, 50, '2023-03-01', 'ST_CLERK'),
    (302, 'Ravi',  'Kumar',  55000, 50, '2023-05-15', 'ST_CLERK'),
    (303, 'Priya', 'Nair',   70000, 80, '2023-07-20', 'MK_REP'),
]

try:
    cursor.executemany("""
        INSERT INTO employees
            (employee_id, first_name, last_name, salary, department_id, hire_date, job_id)
        VALUES
            (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7)
    """, employees_data)

    conn.commit()
    print(f"{cursor.rowcount} employees inserted successfully.")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `executemany()` sends all rows in a single database round-trip — much faster than looping.
- Data is a list of tuples; each tuple maps to one INSERT row via positional bind variables.
- cx_Oracle optimises `executemany()` internally using array binding.
- `cursor.rowcount` after executemany() returns the total rows inserted.
- Preferred enterprise pattern for bulk data loading.

---

### Q7 — Fetch Results Using fetchmany() for Pagination

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT employee_id, first_name, salary
    FROM employees
    ORDER BY salary DESC
""")

batch_size = 5
batch_num  = 1

while True:
    rows = cursor.fetchmany(batch_size)
    if not rows:
        break
    print(f"\n--- Batch {batch_num} ---")
    for row in rows:
        print(f"  ID: {row[0]} | {row[1]} | ₹{row[2]}")
    batch_num += 1

cursor.close()
conn.close()
```

**📝 Explanation:**
- `fetchmany(n)` retrieves exactly n rows per call — memory-efficient for large result sets.
- Loop exits when `fetchmany()` returns an empty list (no more rows).
- Avoids loading thousands of rows into memory with `fetchall()`.
- `cursor.arraysize` can be set to tune the default fetch size: `cursor.arraysize = 100`.
- Key exam concept: knowing when to use `fetchone()` vs `fetchmany()` vs `fetchall()`.

---

## 🟡 INTERMEDIATE LEVEL (Q8–Q14)

---

### Q8 — Call a Stored Procedure

```python
import cx_Oracle

# Oracle Stored Procedure:
# CREATE OR REPLACE PROCEDURE raise_salary(p_emp_id IN NUMBER, p_percent IN NUMBER) AS
# BEGIN
#   UPDATE employees SET salary = salary * (1 + p_percent/100)
#   WHERE employee_id = p_emp_id;
#   COMMIT;
# END;

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    cursor.callproc("raise_salary", [101, 15])   # 15% raise for emp 101
    print("Stored procedure executed successfully.")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.callproc("proc_name", [arg1, arg2])` — calls an Oracle stored procedure.
- Arguments are passed as a Python list in the same order as the procedure's parameters.
- No `conn.commit()` needed here since the procedure contains `COMMIT` internally.
- `callproc` is cx_Oracle's dedicated method for procedures — use `callfunc` for functions.
- Stored procedures are core to enterprise Oracle systems and heavily tested at L1.

---

### Q9 — Call a Function and Capture Return Value

```python
import cx_Oracle

# Oracle Function:
# CREATE OR REPLACE FUNCTION get_annual_salary(p_emp_id IN NUMBER) RETURN NUMBER AS
#   v_sal NUMBER;
# BEGIN
#   SELECT salary * 12 INTO v_sal FROM employees WHERE employee_id = p_emp_id;
#   RETURN v_sal;
# END;

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    annual_salary = cursor.callfunc("get_annual_salary", cx_Oracle.NUMBER, [101])
    print(f"Annual Salary for Employee 101: ₹{annual_salary:,.2f}")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.callfunc("func_name", return_type, [args])` — the return type is mandatory.
- Return type constants: `cx_Oracle.NUMBER`, `cx_Oracle.STRING`, `cx_Oracle.DATE`.
- Key difference: `callproc` for procedures (no return); `callfunc` for functions (has return value).
- The return value is directly usable as a Python variable.
- Exam tip: forgetting the return type argument in `callfunc` causes a TypeError.

---

### Q10 — Using OUT Parameters with Stored Procedures

```python
import cx_Oracle

# Oracle Procedure:
# CREATE OR REPLACE PROCEDURE get_emp_details(
#   p_emp_id IN  NUMBER,
#   p_name   OUT VARCHAR2,
#   p_salary OUT NUMBER
# ) AS
# BEGIN
#   SELECT first_name || ' ' || last_name, salary
#   INTO p_name, p_salary
#   FROM employees WHERE employee_id = p_emp_id;
# END;

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    out_name   = cursor.var(cx_Oracle.STRING)
    out_salary = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc("get_emp_details", [101, out_name, out_salary])

    print(f"Employee Name  : {out_name.getvalue()}")
    print(f"Employee Salary: ₹{out_salary.getvalue():,.2f}")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.var(cx_Oracle.STRING)` / `cursor.var(cx_Oracle.NUMBER)` — creates OUT parameter containers.
- `.getvalue()` retrieves the value after the procedure populates the OUT parameter.
- OUT parameters are how Oracle procedures return multiple values simultaneously.
- The var object is passed in the args list alongside IN parameters.
- Exam frequently tests: IN vs OUT vs IN OUT — only OUT and IN OUT use `cursor.var()`.

---

### Q11 — Execute Dynamic SQL with String Filters

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

def get_employees_by_filters(min_salary=None, dept_id=None):
    query  = "SELECT employee_id, first_name, salary FROM employees WHERE 1=1"
    params = {}

    if min_salary is not None:
        query += " AND salary >= :min_salary"
        params["min_salary"] = min_salary

    if dept_id is not None:
        query += " AND department_id = :dept_id"
        params["dept_id"] = dept_id

    query += " ORDER BY salary DESC"

    cursor.execute(query, params)
    return cursor.fetchall()

# Usage
results = get_employees_by_filters(min_salary=10000, dept_id=60)
for r in results:
    print(f"ID: {r[0]} | Name: {r[1]} | Salary: ₹{r[2]}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `WHERE 1=1` — allows conditional AND clauses to be appended cleanly without if-first logic.
- Dictionary `params` is built dynamically alongside the query string.
- cx_Oracle accepts a dict of bind variables — only the keys referenced in the query are used.
- Critical: never use f-strings or `%s` formatting for values — always use bind variables.
- This pattern powers search/filter APIs in real enterprise applications.

---

### Q12 — Using Context Manager (with Statement)

```python
import cx_Oracle

with cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL") as conn:
    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT d.department_name,
                   COUNT(e.employee_id)   AS emp_count,
                   ROUND(AVG(e.salary),2) AS avg_salary
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_name
            HAVING COUNT(e.employee_id) > 0
            ORDER BY avg_salary DESC
        """)

        print(f"{'Department':<25} {'Headcount':>10} {'Avg Salary':>12}")
        print("-" * 50)
        for dept, count, avg_sal in cursor:
            print(f"{dept:<25} {count:>10} {avg_sal:>12.2f}")
```

**📝 Explanation:**
- `with cx_Oracle.connect(...) as conn` — context manager auto-closes connection when block exits.
- `with conn.cursor() as cursor` — auto-closes cursor; no need for explicit `.close()` calls.
- Direct iteration over cursor (`for row in cursor`) streams rows without loading all into memory.
- `LEFT JOIN` + `HAVING COUNT > 0` — includes only departments that have at least one employee.
- Pythonic best practice — use context managers in all production code.

---

### Q13 — Using Connection Pool (SessionPool)

```python
import cx_Oracle

# cx_Oracle uses SessionPool (not create_pool like oracledb)
pool = cx_Oracle.SessionPool(
    user="hr",
    password="hr123",
    dsn="localhost:1521/ORCL",
    min=2,        # Minimum connections kept alive
    max=10,       # Maximum concurrent connections
    increment=1,  # Connections added when pool exhausted
    threaded=True # Enable for multi-threaded applications
)

def get_top_earners(dept_id):
    conn   = pool.acquire()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT first_name, last_name, salary
            FROM employees
            WHERE department_id = :dept
            ORDER BY salary DESC
            FETCH FIRST 3 ROWS ONLY
        """, dept=dept_id)
        return cursor.fetchall()
    finally:
        cursor.close()
        pool.release(conn)   # Returns connection back to pool

# Simulate multiple department lookups
for dept in [50, 60, 80]:
    result = get_top_earners(dept)
    print(f"\nTop 3 Earners in Dept {dept}:")
    for r in result:
        print(f"  {r[0]} {r[1]} — ₹{r[2]}")

pool.close()
```

**📝 Explanation:**
- `cx_Oracle.SessionPool(...)` — cx_Oracle's connection pool (equivalent to oracledb's `create_pool`).
- `pool.acquire()` borrows a connection; `pool.release(conn)` returns it to the pool.
- `threaded=True` — required for multi-threaded web servers (Flask, Django, FastAPI).
- Pool reuses connections — avoids costly Oracle login overhead on every request.
- `FETCH FIRST N ROWS ONLY` — Oracle 12c+ syntax for top-N queries.
- Exam tip: `min`, `max`, `increment`, `threaded` are key SessionPool parameters.

---

### Q14 — Ref Cursor (Returning Result Sets from PL/SQL)

```python
import cx_Oracle

# Oracle Procedure:
# CREATE OR REPLACE PROCEDURE get_dept_employees(
#   p_dept_id IN  NUMBER,
#   p_cursor  OUT SYS_REFCURSOR
# ) AS
# BEGIN
#   OPEN p_cursor FOR
#     SELECT employee_id, first_name, salary
#     FROM employees WHERE department_id = p_dept_id;
# END;

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    ref_cursor = conn.cursor()   # This cursor acts as the OUT SYS_REFCURSOR

    cursor.callproc("get_dept_employees", [60, ref_cursor])

    print("Employees in Department 60:")
    for row in ref_cursor:
        print(f"  ID: {row[0]} | Name: {row[1]} | Salary: ₹{row[2]}")

finally:
    ref_cursor.close()
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `conn.cursor()` creates a second cursor object that acts as the REF CURSOR container.
- cx_Oracle automatically recognises a cursor passed to `callproc` as a REF CURSOR bind.
- `SYS_REFCURSOR` is Oracle's mechanism for returning a full result set from PL/SQL.
- The ref_cursor is iterable in Python just like a normal query cursor.
- Common enterprise pattern: stored procedures return datasets to the application layer.

---

## 🔴 HARD LEVEL (Q15–Q20)

---

### Q15 — Transaction Management with Savepoints

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    # Step 1: Insert a new department
    cursor.execute("""
        INSERT INTO departments (department_id, department_name, location_id)
        VALUES (280, 'AI Research', 1700)
    """)

    # Create a savepoint after the safe first step
    cursor.execute("SAVEPOINT after_dept_insert")

    # Step 2: Insert an employee into that department
    cursor.execute("""
        INSERT INTO employees
            (employee_id, first_name, last_name, salary, department_id, hire_date, job_id)
        VALUES (305, 'Dev', 'Patel', 95000, 280, SYSDATE, 'IT_PROG')
    """)

    # Simulate a business rule failure
    raise Exception("Budget cap exceeded — rolling back employee insert only.")

    conn.commit()
    print("All changes committed.")

except Exception as e:
    print(f"Error: {e}")
    cursor.execute("ROLLBACK TO SAVEPOINT after_dept_insert")
    conn.commit()   # Commit the department insert only
    print("Department saved; employee insert rolled back.")

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `SAVEPOINT name` — marks a partial rollback point within a transaction.
- `ROLLBACK TO SAVEPOINT name` — undoes only work done after the savepoint, not everything.
- cx_Oracle savepoints are executed as SQL strings via `cursor.execute()`.
- Demonstrates **partial transaction recovery** — critical in enterprise multi-step workflows.
- Exam question: "What happens if you call `conn.close()` without committing?" → Auto-rollback.

---

### Q16 — Analytical Window Functions via Python

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        employee_id,
        first_name,
        department_id,
        salary,
        RANK()       OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank,
        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank,
        ROUND(salary / SUM(salary) OVER (PARTITION BY department_id) * 100, 2) AS salary_pct,
        LAG(salary)  OVER (PARTITION BY department_id ORDER BY salary DESC)    AS prev_higher_sal,
        LEAD(salary) OVER (PARTITION BY department_id ORDER BY salary DESC)    AS next_lower_sal
    FROM employees
    WHERE department_id IN (60, 80)
    ORDER BY department_id, dept_rank
""")

# Dynamically build header from cursor.description
columns = [col[0] for col in cursor.description]
print(" | ".join(f"{c:<18}" for c in columns))
print("-" * 110)
for row in cursor.fetchall():
    print(" | ".join(f"{str(v):<18}" for v in row))

cursor.close()
conn.close()
```

**📝 Explanation:**
- `RANK()` skips numbers after ties (1,1,3); `DENSE_RANK()` does not (1,1,2).
- `PARTITION BY` resets the window per department — acts like GROUP BY for window functions.
- `LAG` / `LEAD` — access the previous / next row's value in the sorted window.
- `cursor.description` — list of 7-tuples; index `[0]` is the column name.
- Window functions cannot be in WHERE — wrap in a subquery to filter on them.

---

### Q17 — Hierarchical Query (CONNECT BY) for Org Chart

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        LEVEL,
        LPAD(' ', (LEVEL - 1) * 4) || first_name || ' ' || last_name AS emp_hierarchy,
        employee_id,
        manager_id,
        salary
    FROM employees
    START WITH manager_id IS NULL
    CONNECT BY PRIOR employee_id = manager_id
    ORDER SIBLINGS BY last_name
""")

print(f"{'Lvl':<5} {'Hierarchy':<40} {'Emp ID':<8} {'Mgr ID':<8} {'Salary':>10}")
print("-" * 75)
for level, hierarchy, emp_id, mgr_id, salary in cursor.fetchall():
    print(f"{level:<5} {hierarchy:<40} {emp_id:<8} {str(mgr_id):<8} {salary:>10}")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `CONNECT BY PRIOR employee_id = manager_id` — traverses the tree downward from root.
- `START WITH manager_id IS NULL` — identifies root nodes (employees with no manager).
- `LEVEL` pseudo-column — depth of current row in the hierarchy (1 = root/CEO).
- `LPAD(' ', (LEVEL-1)*4)` — indents each level by 4 spaces for visual tree display.
- `ORDER SIBLINGS BY` — sorts children at each level without breaking the hierarchy.
- Unique to Oracle SQL — not in standard ANSI SQL.

---

### Q18 — Bulk Data Processing with RETURNING INTO Clause

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    emp_ids     = cursor.arrayvar(cx_Oracle.NUMBER, 100)
    new_sals    = cursor.arrayvar(cx_Oracle.NUMBER, 100)

    cursor.execute("""
        UPDATE employees
        SET salary = salary * 1.12
        WHERE department_id = 60
        AND job_id = 'IT_PROG'
        RETURNING employee_id, salary INTO :emp_ids, :new_sals
    """, emp_ids=emp_ids, new_sals=new_sals)

    conn.commit()

    updated_ids  = emp_ids.getvalue()
    updated_sals = new_sals.getvalue()

    print(f"Updated {len(updated_ids)} employees:")
    for eid, sal in zip(updated_ids, updated_sals):
        print(f"  Emp {int(eid)}: New Salary = ₹{sal:,.2f}")

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Error: {error_obj.message}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- `cursor.arrayvar(cx_Oracle.NUMBER, max_rows)` — creates an array bind variable for multiple returned values.
- `RETURNING INTO` — fetches updated values without a separate SELECT query.
- `.getvalue()` retrieves the Python list of values after the UPDATE.
- Eliminates an extra round-trip to the database — key for performance in enterprise apps.
- Used in audit logging, change tracking, and post-update confirmation workflows.

---

### Q19 — Execute PL/SQL Anonymous Block with Exception Handling

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

emp_id     = 9999   # Non-existent employee
out_message = cursor.var(cx_Oracle.STRING)

plsql_block = """
DECLARE
    v_salary   employees.salary%TYPE;
    v_name     VARCHAR2(100);
BEGIN
    SELECT first_name || ' ' || last_name, salary
    INTO v_name, v_salary
    FROM employees
    WHERE employee_id = :emp_id;

    :message := 'Employee: ' || v_name || ' | Salary: ' || TO_CHAR(v_salary);

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        :message := 'ERROR: Employee ID ' || :emp_id || ' does not exist.';
    WHEN TOO_MANY_ROWS THEN
        :message := 'ERROR: Multiple records found.';
    WHEN OTHERS THEN
        :message := 'UNEXPECTED ERROR: ' || SQLERRM;
END;
"""

try:
    cursor.execute(plsql_block, emp_id=emp_id, message=out_message)
    print(out_message.getvalue())

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"Python DB Error [{error_obj.code}]: {error_obj.message}")

finally:
    cursor.close()
    conn.close()
```

**📝 Explanation:**
- Full PL/SQL anonymous block executed via `cursor.execute()` — same method as SQL.
- `%TYPE` — anchors PL/SQL variable type to the actual column definition (best practice).
- `NO_DATA_FOUND`, `TOO_MANY_ROWS`, `WHEN OTHERS` — standard PL/SQL exception handlers.
- `SQLERRM` — Oracle built-in returning the error message for `WHEN OTHERS`.
- `cursor.var(cx_Oracle.STRING)` used for the OUT bind variable `:message`.
- PL/SQL blocks can mix IN bind variables (`:emp_id`) and OUT vars (`:message`) freely.

---

### Q20 — Full Enterprise Pattern: Audit Log with Sequence

```python
import cx_Oracle
from datetime import datetime

# Oracle objects assumed:
# SEQUENCE : emp_audit_seq
# TABLE    : emp_audit_log (log_id, emp_id, action, old_salary, new_salary, changed_by, changed_at)

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

def apply_salary_change_with_audit(emp_id: int, new_salary: float, changed_by: str):
    try:
        # Fetch current salary before update
        cursor.execute(
            "SELECT salary FROM employees WHERE employee_id = :emp_id",
            emp_id=emp_id
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Employee {emp_id} not found.")

        old_salary = row[0]

        # Apply salary update
        cursor.execute("""
            UPDATE employees
            SET salary = :new_sal
            WHERE employee_id = :emp_id
        """, new_sal=new_salary, emp_id=emp_id)

        # Insert audit record using Oracle SEQUENCE for unique log_id
        cursor.execute("""
            INSERT INTO emp_audit_log
                (log_id, emp_id, action, old_salary, new_salary, changed_by, changed_at)
            VALUES
                (emp_audit_seq.NEXTVAL, :emp_id, 'SALARY_UPDATE',
                 :old_sal, :new_sal, :by, SYSDATE)
        """, emp_id=emp_id, old_sal=old_salary, new_sal=new_salary, by=changed_by)

        conn.commit()
        print(f"✅ Salary updated: ₹{old_salary:,.2f} → ₹{new_salary:,.2f}")
        print(f"   Audit logged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by {changed_by}")

    except ValueError as ve:
        print(f"Business Error: {ve}")
        conn.rollback()

    except cx_Oracle.DatabaseError as e:
        error_obj, = e.args
        print(f"DB Error [{error_obj.code}]: {error_obj.message}")
        conn.rollback()

# Execute
apply_salary_change_with_audit(emp_id=101, new_salary=18000.00, changed_by="admin_user")

cursor.close()
conn.close()
```

**📝 Explanation:**
- `emp_audit_seq.NEXTVAL` — Oracle SEQUENCE generates unique auto-incrementing IDs (Oracle's alternative to AUTO_INCREMENT).
- Full audit pattern: fetch old value → apply DML → log both values in one atomic transaction.
- `SYSDATE` inside SQL avoids clock skew issues from Python-side timestamps.
- All three operations (SELECT + UPDATE + INSERT) committed together or rolled back together.
- Production-grade pattern used in banking, insurance, ERP systems worldwide.
- Tests: sequences, multi-statement transactions, audit trails, cx_Oracle error object unpacking.

---

## 📊 Quick Reference Summary — Set 1 (cx_Oracle)

| # | Topic | Level | Key cx_Oracle Concept |
|---|-------|-------|----------------------|
| Q1 | SELECT + bind variable | 🟢 Normal | `connect()`, named binds, `fetchall()` |
| Q2 | INSERT + error handling | 🟢 Normal | `IntegrityError`, `error_obj.code` |
| Q3 | UPDATE + rowcount | 🟢 Normal | `cursor.rowcount`, `commit()` |
| Q4 | DELETE + rowcount check | 🟢 Normal | `rollback()`, `rowcount == 0` |
| Q5 | JOIN + fetchone() | 🟢 Normal | `fetchone()`, None check |
| Q6 | Batch insert executemany() | 🟢 Normal | `executemany()`, array binding |
| Q7 | Pagination fetchmany() | 🟢 Normal | `fetchmany(n)`, `arraysize` |
| Q8 | Call stored procedure | 🟡 Medium | `callproc()` |
| Q9 | Call function + return | 🟡 Medium | `callfunc()`, `cx_Oracle.NUMBER` |
| Q10 | OUT parameters | 🟡 Medium | `cursor.var()`, `.getvalue()` |
| Q11 | Dynamic SQL builder | 🟡 Medium | `WHERE 1=1`, dict params |
| Q12 | Context manager | 🟡 Medium | `with connect()`, auto-close |
| Q13 | Connection pool | 🟡 Medium | `SessionPool`, `acquire/release` |
| Q14 | REF CURSOR | 🟡 Medium | `conn.cursor()` as OUT bind |
| Q15 | Savepoints | 🔴 Hard | `SAVEPOINT`, `ROLLBACK TO` |
| Q16 | Window functions | 🔴 Hard | `RANK`, `LAG/LEAD`, `PARTITION BY` |
| Q17 | CONNECT BY hierarchy | 🔴 Hard | `LEVEL`, `PRIOR`, `START WITH` |
| Q18 | RETURNING INTO | 🔴 Hard | `arrayvar()`, bulk return |
| Q19 | PL/SQL anonymous block | 🔴 Hard | `DECLARE/BEGIN/EXCEPTION/END` |
| Q20 | Audit log + Sequence | 🔴 Hard | `NEXTVAL`, full transaction |

---

## ⚡ cx_Oracle vs oracledb — Quick Cheat Sheet

| Feature | cx_Oracle | oracledb |
|---------|-----------|----------|
| Import | `import cx_Oracle` | `import oracledb` |
| Connect | `cx_Oracle.connect("u","p","dsn")` | `oracledb.connect(user=,password=,dsn=)` |
| Pool | `cx_Oracle.SessionPool(...)` | `oracledb.create_pool(...)` |
| Pool acquire | `pool.acquire()` | `pool.acquire()` (same) |
| Pool release | `pool.release(conn)` | Auto on context exit |
| NUMBER type | `cx_Oracle.NUMBER` | `oracledb.NUMBER` |
| STRING type | `cx_Oracle.STRING` | `oracledb.STRING` |
| Error object | `e.args` unpack needed | `e.args` unpack needed |
| Thin mode | Not supported | Supported (no client) |
| Oracle Client | Required always | Optional (Thin mode) |

---

*Set 1 (cx_Oracle Edition) — Capgemini L1 Oracle + Python DB Connectivity Exam*
*Normal → Hard | Bind Variables, DML, Procedures, Functions, Pools, PL/SQL, Transactions*
