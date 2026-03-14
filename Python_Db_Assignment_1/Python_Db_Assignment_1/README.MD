## Overview

This project contains four Python tasks.  
Each task includes:

1. **A DB setup file** – creates and seeds the necessary table  
2. **An entity (class) file**  
3. **A solution file** – contains the required method  

**Always run the DB setup file first**, then run the solution file.

---

## Question 1 – Insert Customer Records

**Task:**  
Write a method `add_customer_details(self, customer_list)` that inserts customer objects into the `customer` table.  
Each customer has: `customer_id`, `name`, `email`, `phone`.

**Files:**
- `db_setup.py`
- `customer_entity.py`
- `customer_solution.py`

**How to run:**
python3 db_setup.py
python3 customer_solution.py

---

## Question 2: Insert Attendance Records

**Task:**  
Write a method `record_attendance(self, attendance_list)` that inserts attendance data into an `attendance` table.  
Each attendance record includes:
- employee_id  
- date  
- status  

---

## Question 3: Insert Multiple Rows in a Single Query

**Task:**  
Write a method `bulk_insert_books(self, book_list)` that inserts multiple book records into a `books` table using a single `executemany()` call.  
Each book has:
- book_id  
- title  
- author  
- price  

---

## Question 4: Search Customer by ID

**Task:**  
Write a method `search_customer_by_id(self, customer_id)` that retrieves a customer record from the `customer` table using the given ID.  
- If the record exists → return a `Customer` object  
- If not found → return `None`  