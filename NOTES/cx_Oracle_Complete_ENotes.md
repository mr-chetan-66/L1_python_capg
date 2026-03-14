# 📘 E-Notes: cx_Oracle Module in Python
## Complete Guide to Oracle Database Connectivity
### Prepared for Capgemini L1 Exam | Database Connectivity with Python

---

## 📑 Table of Contents

1. [Introduction to cx_Oracle](#1-introduction-to-cx_oracle)
2. [Installation and Setup](#2-installation-and-setup)
3. [Connecting to Oracle Database](#3-connecting-to-oracle-database)
4. [Cursor Object](#4-cursor-object)
5. [Executing SQL Queries](#5-executing-sql-queries)
6. [Fetching Data](#6-fetching-data)
7. [Bind Variables](#7-bind-variables)
8. [DML Operations](#8-dml-operations-insert-update-delete)
9. [Transaction Management](#9-transaction-management)
10. [Stored Procedures and Functions](#10-stored-procedures-and-functions)
11. [PL/SQL Blocks](#11-plsql-anonymous-blocks)
12. [Connection Pooling](#12-connection-pooling-sessionpool)
13. [Error Handling](#13-error-handling)
14. [LOB Data Types](#14-lob-data-types)
15. [cx_Oracle Data Type Constants](#15-cx_oracle-data-type-constants)
16. [Context Managers](#16-context-managers)
17. [Best Practices](#17-best-practices)
18. [Quick Reference Cheat Sheet](#18-quick-reference-cheat-sheet)

---

## 1. Introduction to cx_Oracle

### What is cx_Oracle?
`cx_Oracle` is a Python **extension module** that enables Python programs to connect to and interact with **Oracle Database**. It acts as the bridge between Python applications and Oracle RDBMS.

```
Python Application
       │
       ▼
  cx_Oracle Module
       │
       ▼
Oracle Instant Client (C Libraries)
       │
       ▼
Oracle Database Server
```

### Key Features
- Full support for Oracle SQL and PL/SQL
- Support for stored procedures, functions, and REF cursors
- Connection pooling via `SessionPool`
- Support for CLOB, BLOB, and other Oracle data types
- Bind variables for performance and security
- Batch operations using `executemany()`
- Transaction control (commit, rollback, savepoints)

### cx_Oracle vs oracledb
| Feature | cx_Oracle | oracledb (successor) |
|---------|-----------|----------------------|
| Module name | `cx_Oracle` | `oracledb` |
| Oracle Client | Always required | Optional (Thin mode) |
| Thin mode | ❌ Not supported | ✅ Supported |
| Status | Stable, widely used | New (replacement) |
| Exam relevance | ✅ High (Capgemini L1) | Moderate |

> **Note:** `cx_Oracle` is still the most commonly used module in enterprise environments and exams. `oracledb` is its official successor but the API is mostly identical.

---

## 2. Installation and Setup

### Step 1 — Install cx_Oracle

```bash
pip install cx_Oracle
```

### Step 2 — Install Oracle Instant Client
cx_Oracle requires Oracle Instant Client C libraries.

1. Download from: https://www.oracle.com/database/technologies/instant-client.html
2. Choose: **Basic** or **Basic Light** package
3. Extract to a folder, e.g., `C:\oracle\instantclient_21_1` (Windows)

### Step 3 — Initialize Oracle Client in Code (if needed)

```python
import cx_Oracle

# Only needed if Oracle Client is NOT in PATH
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_1")
```

### Step 4 — Verify Installation

```python
import cx_Oracle
print(cx_Oracle.__version__)           # cx_Oracle version
print(cx_Oracle.clientversion())       # Oracle Client version tuple e.g. (21, 1, 0, 0, 0)
```

### Connection String Formats

| Format | Example |
|--------|---------|
| Easy Connect | `"localhost:1521/ORCL"` |
| Easy Connect with protocol | `"localhost:1521/ORCL"` |
| TNS Alias | `"ORCL"` (from tnsnames.ora) |
| Full DSN | `cx_Oracle.makedsn("host", 1521, sid="ORCL")` |
| Service Name DSN | `cx_Oracle.makedsn("host", 1521, service_name="ORCL")` |

```python
# Using makedsn
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="ORCL")
conn = cx_Oracle.connect("hr", "hr123", dsn)
```

---

## 3. Connecting to Oracle Database

### Basic Connection

```python
import cx_Oracle

# Method 1: Positional arguments (most common)
conn = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")

# Method 2: Keyword arguments
conn = cx_Oracle.connect(user="hr", password="hr123", dsn="localhost:1521/ORCL")

# Method 3: Single connection string
conn = cx_Oracle.connect("hr/hr123@localhost:1521/ORCL")

print(f"Connected to Oracle version: {conn.version}")
conn.close()
```

### Connection Properties

```python
conn = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")

print(conn.version)       # Oracle DB version e.g. '19.0.0.0.0'
print(conn.username)      # Connected user e.g. 'HR'
print(conn.dsn)           # DSN string
print(conn.autocommit)    # Auto-commit status (default: False)

conn.close()
```

### Setting Autocommit

```python
conn = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")

# Enable auto-commit (not recommended for enterprise use)
conn.autocommit = True

# Disable auto-commit (default — recommended)
conn.autocommit = False
```

> ⚠️ **Important:** cx_Oracle does **NOT** auto-commit by default.  
> Always call `conn.commit()` after INSERT / UPDATE / DELETE.

---

## 4. Cursor Object

A **cursor** is an object used to execute SQL statements and manage result sets.

```python
conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()   # Create cursor from connection
```

### Cursor Attributes

| Attribute | Description |
|-----------|-------------|
| `cursor.rowcount` | Number of rows affected by last DML |
| `cursor.description` | Metadata of columns in result set |
| `cursor.arraysize` | Default fetch size (default: 100) |
| `cursor.rowfactory` | Factory function for custom row objects |

```python
cursor.execute("SELECT employee_id, first_name, salary FROM employees")

# cursor.description: list of 7-tuples
# (name, type_code, display_size, internal_size, precision, scale, null_ok)
for col in cursor.description:
    print(f"Column: {col[0]}, Type: {col[1]}")
```

### Tuning Fetch Size with arraysize

```python
cursor.arraysize = 500   # Fetch 500 rows at a time from Oracle (reduces round-trips)
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
```

---

## 5. Executing SQL Queries

### execute() — Single Statement

```python
# Simple SELECT
cursor.execute("SELECT * FROM employees")

# With bind variables (named)
cursor.execute("SELECT * FROM employees WHERE department_id = :dept", dept=60)

# With bind variables (positional)
cursor.execute("SELECT * FROM employees WHERE department_id = :1", (60,))

# With bind variables (dictionary)
cursor.execute("SELECT * FROM employees WHERE department_id = :dept", {"dept": 60})
```

### executemany() — Batch Operations

```python
data = [
    (301, 'Amit', 'Shah',   55000, 60),
    (302, 'Riya', 'Joshi',  62000, 80),
    (303, 'Kiran','Patel',  48000, 50),
]

cursor.executemany("""
    INSERT INTO employees (employee_id, first_name, last_name, salary, department_id)
    VALUES (:1, :2, :3, :4, :5)
""", data)

conn.commit()
print(f"Inserted: {cursor.rowcount} rows")
```

> ✅ `executemany()` uses **array binding** — sends all rows in ONE Oracle round-trip.  
> Much faster than calling `execute()` in a loop.

---

## 6. Fetching Data

### fetchone() — Single Row

```python
cursor.execute("SELECT employee_id, first_name FROM employees WHERE employee_id = :id", id=101)
row = cursor.fetchone()   # Returns tuple or None

if row:
    print(f"ID: {row[0]}, Name: {row[1]}")
else:
    print("Not found")
```

### fetchmany() — N Rows at a Time

```python
cursor.execute("SELECT employee_id, first_name, salary FROM employees ORDER BY salary DESC")

while True:
    rows = cursor.fetchmany(5)   # Fetch 5 rows at a time
    if not rows:
        break
    for row in rows:
        print(row)
```

### fetchall() — All Rows

```python
cursor.execute("SELECT * FROM employees WHERE department_id = :dept", dept=60)
rows = cursor.fetchall()   # Returns list of tuples

for row in rows:
    print(row)
```

### Direct Iteration (Memory Efficient)

```python
cursor.execute("SELECT employee_id, first_name, salary FROM employees")

for row in cursor:   # Streams rows without loading all into memory
    print(row)
```

### Comparison of Fetch Methods

| Method | Returns | Best Used When |
|--------|---------|----------------|
| `fetchone()` | Single tuple / None | Expecting exactly one row (PK lookup) |
| `fetchmany(n)` | List of n tuples | Pagination, large datasets |
| `fetchall()` | List of all tuples | Small to medium result sets |
| `for row in cursor` | One row at a time | Very large datasets (streaming) |

---

## 7. Bind Variables

Bind variables are **placeholders** in SQL replaced by actual values at execution time.

### Why Use Bind Variables?
1. **Security** — Prevents SQL injection attacks
2. **Performance** — Oracle reuses the parsed SQL plan (cursor sharing)
3. **Type safety** — Oracle handles type conversion automatically

### Named Bind Variables (Recommended)

```python
# Single value
cursor.execute("SELECT * FROM employees WHERE employee_id = :emp_id", emp_id=101)

# Multiple values
cursor.execute("""
    SELECT * FROM employees
    WHERE department_id = :dept AND salary > :min_sal
""", dept=60, min_sal=5000)
```

### Positional Bind Variables

```python
cursor.execute("""
    INSERT INTO employees (employee_id, first_name, salary)
    VALUES (:1, :2, :3)
""", (301, 'Raj', 70000))
```

### Dictionary Bind Variables

```python
params = {"dept": 60, "min_sal": 8000}
cursor.execute("SELECT * FROM employees WHERE department_id = :dept AND salary > :min_sal", params)
```

> ❌ **NEVER do this — SQL Injection risk:**
> ```python
> dept = 60
> cursor.execute(f"SELECT * FROM employees WHERE department_id = {dept}")  # WRONG
> ```

---

## 8. DML Operations (INSERT, UPDATE, DELETE)

### INSERT

```python
conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO employees
            (employee_id, first_name, last_name, salary, department_id, hire_date, job_id)
        VALUES
            (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7)
    """, (310, 'Neha', 'Gupta', 68000, 60, '2024-06-01', 'IT_PROG'))

    conn.commit()
    print(f"Inserted {cursor.rowcount} row(s)")

except cx_Oracle.IntegrityError as e:
    error_obj, = e.args
    print(f"Integrity Error: {error_obj.message}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
```

### UPDATE

```python
cursor.execute("""
    UPDATE employees
    SET salary = salary * 1.10
    WHERE department_id = :dept AND salary < :threshold
""", dept=60, threshold=10000)

print(f"Updated {cursor.rowcount} row(s)")
conn.commit()
```

### DELETE

```python
cursor.execute("""
    DELETE FROM employees
    WHERE employee_id = :emp_id
""", emp_id=310)

if cursor.rowcount == 0:
    print("No record found.")
else:
    print(f"Deleted {cursor.rowcount} row(s)")
conn.commit()
```

### RETURNING INTO (Get Updated Values)

```python
emp_ids  = cursor.arrayvar(cx_Oracle.NUMBER, 100)
new_sals = cursor.arrayvar(cx_Oracle.NUMBER, 100)

cursor.execute("""
    UPDATE employees
    SET salary = salary * 1.15
    WHERE department_id = 60
    RETURNING employee_id, salary INTO :eids, :sals
""", eids=emp_ids, sals=new_sals)

conn.commit()

for eid, sal in zip(emp_ids.getvalue(), new_sals.getvalue()):
    print(f"Emp {int(eid)}: New Salary = {sal:.2f}")
```

---

## 9. Transaction Management

### commit() and rollback()

```python
try:
    cursor.execute("INSERT INTO departments VALUES (290, 'DevOps', 1700, NULL)")
    cursor.execute("INSERT INTO employees (employee_id, ...) VALUES (320, ...)")
    conn.commit()       # Both succeed → commit
    print("Transaction committed.")

except cx_Oracle.DatabaseError as e:
    conn.rollback()     # Either fails → rollback both
    print("Transaction rolled back.")
```

### Savepoints (Partial Rollback)

```python
try:
    cursor.execute("INSERT INTO departments VALUES (291, 'MLOps', 1700, NULL)")
    cursor.execute("SAVEPOINT after_dept")      # Mark a point

    cursor.execute("INSERT INTO employees ...")  # This may fail

    conn.commit()

except Exception:
    cursor.execute("ROLLBACK TO SAVEPOINT after_dept")  # Only undo after savepoint
    conn.commit()   # Commit what came before the savepoint
```

### Transaction Rules Summary

| Operation | Effect |
|-----------|--------|
| `conn.commit()` | Permanently saves all pending DML |
| `conn.rollback()` | Cancels all DML since last commit |
| `conn.close()` without commit | **Auto-rollback** — changes are lost |
| `cx_Oracle` default | `autocommit = False` |

---

## 10. Stored Procedures and Functions

### callproc() — Call Stored Procedure

```python
# Oracle Procedure: raise_salary(p_emp_id IN NUMBER, p_percent IN NUMBER)

cursor.callproc("raise_salary", [101, 10])   # 10% raise for emp 101
print("Procedure executed.")
```

### callfunc() — Call Stored Function

```python
# Oracle Function: get_annual_salary(p_emp_id IN NUMBER) RETURN NUMBER

annual_sal = cursor.callfunc("get_annual_salary", cx_Oracle.NUMBER, [101])
print(f"Annual Salary: ₹{annual_sal:,.2f}")
```

### OUT Parameters

```python
# Procedure: get_emp_details(p_id IN NUMBER, p_name OUT VARCHAR2, p_sal OUT NUMBER)

out_name = cursor.var(cx_Oracle.STRING)
out_sal  = cursor.var(cx_Oracle.NUMBER)

cursor.callproc("get_emp_details", [101, out_name, out_sal])

print(f"Name  : {out_name.getvalue()}")
print(f"Salary: {out_sal.getvalue()}")
```

### IN OUT Parameters

```python
# Procedure: adjust_salary(p_sal IN OUT NUMBER, p_factor IN NUMBER)

inout_sal = cursor.var(cx_Oracle.NUMBER)
inout_sal.setvalue(0, 10000)   # Set initial value

cursor.callproc("adjust_salary", [inout_sal, 1.2])
print(f"Adjusted Salary: {inout_sal.getvalue()}")
```

### REF CURSOR (Procedure Returns Result Set)

```python
# Procedure: get_dept_employees(p_dept IN NUMBER, p_cur OUT SYS_REFCURSOR)

ref_cur = conn.cursor()   # Create a cursor to act as REF CURSOR container
cursor.callproc("get_dept_employees", [60, ref_cur])

for row in ref_cur:
    print(row)

ref_cur.close()
```

### Summary: callproc vs callfunc

| Feature | `callproc` | `callfunc` |
|---------|-----------|-----------|
| Used for | Stored Procedures | Stored Functions |
| Return value | None (use OUT vars) | Direct return value |
| Syntax | `callproc("name", [args])` | `callfunc("name", return_type, [args])` |
| Return type arg | Not needed | **Mandatory** |

---

## 11. PL/SQL Anonymous Blocks

Execute full PL/SQL blocks directly from Python using `cursor.execute()`.

```python
out_msg = cursor.var(cx_Oracle.STRING)

plsql = """
DECLARE
    v_name   VARCHAR2(100);
    v_salary employees.salary%TYPE;
BEGIN
    SELECT first_name || ' ' || last_name, salary
    INTO v_name, v_salary
    FROM employees
    WHERE employee_id = :emp_id;

    :result := 'Name: ' || v_name || ', Salary: ' || TO_CHAR(v_salary);

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        :result := 'Employee not found.';
    WHEN OTHERS THEN
        :result := 'Error: ' || SQLERRM;
END;
"""

cursor.execute(plsql, emp_id=101, result=out_msg)
print(out_msg.getvalue())
```

### PL/SQL Block Structure

```
DECLARE       ← Optional: declare variables
    variable_name  datatype;
BEGIN         ← Required: executable statements
    -- SQL and PL/SQL statements
EXCEPTION     ← Optional: error handling
    WHEN exception_name THEN ...
END;          ← Required: end of block
```

### Common PL/SQL Exceptions

| Exception | Trigger |
|-----------|---------|
| `NO_DATA_FOUND` | SELECT INTO returns zero rows |
| `TOO_MANY_ROWS` | SELECT INTO returns more than one row |
| `ZERO_DIVIDE` | Division by zero |
| `VALUE_ERROR` | Type/size mismatch |
| `WHEN OTHERS` | Catches all unhandled exceptions |
| `SQLERRM` | Returns error message text |
| `SQLCODE` | Returns error code number |

---

## 12. Connection Pooling (SessionPool)

Connection pooling reuses database connections instead of creating new ones each time — critical for performance in enterprise web applications.

### Creating a Session Pool

```python
import cx_Oracle

pool = cx_Oracle.SessionPool(
    user      = "hr",
    password  = "hr123",
    dsn       = "localhost:1521/ORCL",
    min       = 2,        # Min connections always kept alive
    max       = 10,       # Max concurrent connections allowed
    increment = 1,        # Connections added when pool is full
    threaded  = True,     # Required for multi-threaded apps
    getmode   = cx_Oracle.SPOOL_ATTRVAL_WAIT  # Wait if pool exhausted
)
```

### Using the Pool

```python
def query_employees(dept_id):
    conn   = pool.acquire()          # Borrow connection from pool
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT first_name, salary FROM employees WHERE department_id = :d",
            d=dept_id
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        pool.release(conn)           # Return connection to pool

result = query_employees(60)
pool.close()                         # Shutdown pool when app exits
```

### SessionPool Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min` | 1 | Connections always open |
| `max` | 2 | Maximum connections |
| `increment` | 1 | How many to create when pool grows |
| `threaded` | False | Set True for multi-threaded use |
| `getmode` | WAIT | What to do when pool is exhausted |
| `homogeneous` | True | All connections use same credentials |

### Pool Acquire Modes

| Mode | Constant | Behaviour |
|------|----------|-----------|
| Wait | `SPOOL_ATTRVAL_WAIT` | Block until connection available |
| No Wait | `SPOOL_ATTRVAL_NOWAIT` | Raise error immediately if pool full |
| Force Get | `SPOOL_ATTRVAL_FORCEGET` | Create beyond max (not recommended) |

---

## 13. Error Handling

### cx_Oracle Exception Hierarchy

```
Exception
└── cx_Oracle.Error
    ├── cx_Oracle.DatabaseError       ← Most common
    │   ├── cx_Oracle.IntegrityError  ← Constraint violations
    │   ├── cx_Oracle.DataError       ← Data conversion issues
    │   └── cx_Oracle.OperationalError
    ├── cx_Oracle.InterfaceError      ← API misuse
    └── cx_Oracle.NotSupportedError   ← Feature not available
```

### Handling Errors — Full Pattern

```python
import cx_Oracle

conn   = cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL")
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO employees (employee_id, first_name, last_name, salary, hire_date, job_id)
        VALUES (:1, :2, :3, :4, SYSDATE, :5)
    """, (101, 'Test', 'User', 50000, 'IT_PROG'))

    conn.commit()

except cx_Oracle.IntegrityError as e:
    error_obj, = e.args
    print(f"[INTEGRITY] Code: {error_obj.code} | Msg: {error_obj.message}")
    # ORA-00001 = unique constraint violated

except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(f"[DB ERROR] Code: {error_obj.code} | Msg: {error_obj.message}")
    conn.rollback()

except cx_Oracle.InterfaceError as e:
    print(f"[INTERFACE ERROR]: {e}")

finally:
    cursor.close()
    conn.close()
```

### Common ORA Error Codes

| ORA Code | Meaning |
|----------|---------|
| ORA-00001 | Unique constraint violated (duplicate PK) |
| ORA-00904 | Invalid column name |
| ORA-00942 | Table or view does not exist |
| ORA-01017 | Invalid username/password |
| ORA-01400 | Cannot insert NULL into NOT NULL column |
| ORA-01403 | No data found (SELECT INTO) |
| ORA-01427 | Single-row subquery returns more than one row |
| ORA-02291 | Integrity constraint violated — parent key not found (FK) |
| ORA-12541 | No listener (connection refused) |

### Error Object Properties

```python
except cx_Oracle.DatabaseError as e:
    error_obj, = e.args          # Unpack the single error object
    print(error_obj.code)        # Integer ORA error number
    print(error_obj.message)     # Full ORA message string
    print(error_obj.context)     # SQL context where error occurred
    print(error_obj.isrecoverable)  # Whether connection is still usable
```

---

## 14. LOB Data Types

Oracle LOBs (Large OBjects) store large text or binary data.

| Oracle Type | Python Type | Description |
|-------------|-------------|-------------|
| `CLOB` | `cx_Oracle.CLOB` | Character Large Object (text) |
| `BLOB` | `cx_Oracle.BLOB` | Binary Large Object (files, images) |
| `NCLOB` | `cx_Oracle.NCLOB` | National Character LOB |

### Reading CLOB Data

```python
cursor.execute("SELECT employee_id, resume_clob FROM emp_resumes WHERE employee_id = :id", id=101)
row = cursor.fetchone()

if row:
    clob_data = row[1].read()   # Read full CLOB content as string
    print(clob_data)
```

### Writing CLOB Data

```python
clob_text = "This is a large resume text..." * 1000

cursor.execute("""
    INSERT INTO emp_resumes (employee_id, resume_clob)
    VALUES (:1, :2)
""", (101, clob_text))

conn.commit()
```

### Auto-convert LOB to String

```python
# Output type handler: auto-read LOBs as strings
def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)

conn.outputtypehandler = output_type_handler
```

---

## 15. cx_Oracle Data Type Constants

### Type Constants for cursor.var() and callfunc()

| Constant | Oracle Type | Python Type |
|----------|-------------|-------------|
| `cx_Oracle.NUMBER` | NUMBER | float |
| `cx_Oracle.STRING` | VARCHAR2 | str |
| `cx_Oracle.DATE` | DATE | datetime |
| `cx_Oracle.TIMESTAMP` | TIMESTAMP | datetime |
| `cx_Oracle.CLOB` | CLOB | LOB object |
| `cx_Oracle.BLOB` | BLOB | LOB object |
| `cx_Oracle.BOOLEAN` | BOOLEAN | bool |
| `cx_Oracle.CURSOR` | REF CURSOR | cursor |
| `cx_Oracle.FIXED_CHAR` | CHAR | str |
| `cx_Oracle.LONG_STRING` | LONG | str |
| `cx_Oracle.BINARY` | RAW | bytes |

### Using cursor.var()

```python
# Create an OUT parameter container
num_var    = cursor.var(cx_Oracle.NUMBER)
str_var    = cursor.var(cx_Oracle.STRING)
date_var   = cursor.var(cx_Oracle.DATE)

# Set a value (for IN OUT parameters)
num_var.setvalue(0, 5000)

# Get value after procedure populates it
result = num_var.getvalue()
```

### Using cursor.arrayvar()

```python
# For RETURNING INTO or array OUT parameters
ids_var  = cursor.arrayvar(cx_Oracle.NUMBER, 200)   # Up to 200 values
sal_var  = cursor.arrayvar(cx_Oracle.NUMBER, 200)

cursor.execute("""
    UPDATE employees SET salary = salary * 1.1
    WHERE department_id = 60
    RETURNING employee_id, salary INTO :ids, :sals
""", ids=ids_var, sals=sal_var)

conn.commit()
print(ids_var.getvalue())   # List of updated employee IDs
```

---

## 16. Context Managers

Use `with` statements for automatic cleanup — Pythonic best practice.

### Connection Context Manager

```python
import cx_Oracle

with cx_Oracle.connect("hr", "hr123", "localhost:1521/ORCL") as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT first_name, salary FROM employees WHERE department_id = :d", d=60)
        for row in cursor:
            print(f"{row[0]}: ₹{row[1]}")
# Connection and cursor auto-closed on block exit
```

### Pool with Context Manager

```python
pool = cx_Oracle.SessionPool("hr", "hr123", "localhost:1521/ORCL", min=2, max=10, increment=1)

with pool.acquire() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        print(f"Total employees: {count}")
# Connection auto-released back to pool

pool.close()
```

---

## 17. Best Practices

### ✅ DO — Always Follow These

```python
# 1. Always use bind variables
cursor.execute("SELECT * FROM employees WHERE id = :id", id=101)  # ✅

# 2. Always close cursor and connection
cursor.close()
conn.close()

# 3. Use context managers
with cx_Oracle.connect(...) as conn:
    with conn.cursor() as cursor:
        ...

# 4. Always handle exceptions
try:
    ...
except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(error_obj.message)
    conn.rollback()
finally:
    cursor.close()
    conn.close()

# 5. Always commit after DML
cursor.execute("INSERT INTO ...")
conn.commit()   # ✅

# 6. Tune arraysize for large queries
cursor.arraysize = 500

# 7. Use executemany() for batch inserts
cursor.executemany("INSERT INTO ...", data_list)  # ✅
```

### ❌ DON'T — Avoid These Mistakes

```python
# 1. Never format SQL with f-strings or % formatting
cursor.execute(f"SELECT * FROM employees WHERE id = {emp_id}")  # ❌ SQL Injection!

# 2. Never forget to commit after DML
cursor.execute("INSERT INTO ...")
# conn.commit() ← Forgetting this means data is lost on close!

# 3. Never use = NULL (always use IS NULL)
cursor.execute("SELECT * FROM employees WHERE commission_pct = NULL")  # ❌ Returns nothing
cursor.execute("SELECT * FROM employees WHERE commission_pct IS NULL") # ✅

# 4. Never insert values using string concatenation
val = "Robert'); DROP TABLE employees;--"
cursor.execute("INSERT INTO t VALUES ('" + val + "')")  # ❌ SQL Injection!
```

---

## 18. Quick Reference Cheat Sheet

### Connection

```python
import cx_Oracle
conn = cx_Oracle.connect("user", "password", "host:port/service")
conn.close()
```

### Cursor Operations

```python
cursor = conn.cursor()
cursor.execute("SQL", bind_vars)
cursor.executemany("SQL", list_of_tuples)
cursor.callproc("proc_name", [args])
cursor.callfunc("func_name", cx_Oracle.NUMBER, [args])
cursor.fetchone()        # → tuple or None
cursor.fetchmany(n)      # → list of n tuples
cursor.fetchall()        # → list of all tuples
cursor.rowcount          # Rows affected by last DML
cursor.description       # Column metadata
cursor.close()
```

### Bind Variables

```python
cursor.execute("... :name", name=value)        # Named
cursor.execute("... :1 :2", (v1, v2))          # Positional
cursor.execute("... :k", {"k": value})          # Dict
```

### OUT Parameters

```python
v = cursor.var(cx_Oracle.NUMBER)   # Create var
v.setvalue(0, 100)                 # Set value (IN OUT)
v.getvalue()                       # Get value after proc
```

### Transaction

```python
conn.commit()                            # Save changes
conn.rollback()                          # Undo changes
cursor.execute("SAVEPOINT sp1")          # Mark savepoint
cursor.execute("ROLLBACK TO SAVEPOINT sp1")  # Partial rollback
```

### Error Handling

```python
except cx_Oracle.DatabaseError as e:
    error_obj, = e.args
    print(error_obj.code)      # ORA error number
    print(error_obj.message)   # ORA error message
    conn.rollback()
```

### Session Pool

```python
pool = cx_Oracle.SessionPool("u", "p", "dsn", min=2, max=10, increment=1, threaded=True)
conn = pool.acquire()
pool.release(conn)
pool.close()
```

### Key Oracle SQL in cx_Oracle

| Task | Oracle Syntax |
|------|--------------|
| Current date | `SYSDATE` |
| Convert string to date | `TO_DATE('2024-01-01', 'YYYY-MM-DD')` |
| NULL substitute | `NVL(col, default)` |
| String concat | `col1 \|\| ' ' \|\| col2` |
| Auto-increment ID | `sequence_name.NEXTVAL` |
| Top N rows | `FETCH FIRST N ROWS ONLY` |
| Dummy table | `FROM DUAL` |
| Substring | `SUBSTR(str, 1, 10)` |
| String position | `INSTR(str, 'find')` |

---

## 📌 Summary — Key Points to Remember for Exam

| # | Key Point |
|---|-----------|
| 1 | `cx_Oracle.connect("user", "pwd", "host:port/svc")` — positional args |
| 2 | Default `autocommit = False` — always call `conn.commit()` after DML |
| 3 | Use bind variables (`:name` or `:1`) — NEVER f-strings for SQL values |
| 4 | `cursor.rowcount` — rows affected after INSERT/UPDATE/DELETE |
| 5 | `fetchone()` → tuple or None; always check `if row:` before accessing |
| 6 | `executemany()` — batch inserts; far faster than looping `execute()` |
| 7 | `callproc()` for procedures; `callfunc()` for functions (needs return type) |
| 8 | OUT params need `cursor.var(type)` and `.getvalue()` after call |
| 9 | `SessionPool` reuses connections — `acquire()` borrows, `release()` returns |
| 10 | Error unpack: `error_obj, = e.args` gives `.code` and `.message` |
| 11 | `SAVEPOINT` + `ROLLBACK TO SAVEPOINT` for partial transaction recovery |
| 12 | REF CURSOR: pass `conn.cursor()` as OUT argument in `callproc()` |
| 13 | `cursor.description[i][0]` gives column name of result set |
| 14 | `cx_Oracle` requires Oracle Instant Client — `oracledb` does not (Thin mode) |
| 15 | Always use `finally` block to close cursor and connection |

---

*cx_Oracle E-Notes | Python Oracle Database Connectivity*
*Covers: Connection, Cursor, DML, Queries, Procedures, Functions, Pooling, PL/SQL, Error Handling*
*Prepared for Capgemini L1 Database Connectivity Examination*
