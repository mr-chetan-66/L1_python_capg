# Python + Oracle DB Connectivity – Practice Problems (20 Questions)

---

## How to Use
- Each problem has its own folder: `problem_1/` through `problem_20/`
- Each folder contains:
  - `<model>.py`              → The entity class (DO NOT modify)
  - `<topic>_management.py`  → The template with `pass` placeholders (FILL THIS)
  - `solution.py`             → Reference solution (check after attempting)
  - `database.properties`    → DB config (update credentials before running)
- The `database.properties` file must be in the same directory when running

---

## Difficulty Progression

| Problem | Topic                    | Concepts Tested                                                  | Difficulty |
|---------|--------------------------|------------------------------------------------------------------|------------|
| 1       | Student                  | SELECT with WHERE + ORDER BY, list return                        | ★☆☆☆☆     |
| 2       | Employee                 | SELECT with BETWEEN, numeric range filter                        | ★★☆☆☆     |
| 3       | Product                  | SELECT with multiple WHERE, date comparison                      | ★★☆☆☆     |
| 4       | Order                    | INSERT + SELECT, commit, error handling                          | ★★★☆☆     |
| 5       | Bank Account             | SELECT + conditional UPDATE, business logic                      | ★★★☆☆     |
| 6       | Doctor                   | SELECT with 2 filters + ORDER BY                                 | ★★☆☆☆     |
| 7       | Library                  | SELECT + conditional UPDATE (atomic logic)                       | ★★★☆☆     |
| 8       | Vehicle Insurance        | Date comparison, SELECT with SYSDATE                             | ★★★☆☆     |
| 9       | Exam Result              | Class-based system, DELETE, Python calc                          | ★★★★☆     |
| 10      | Vehicle Rental           | Class-based, INSERT + calculated fields + UPDATE                 | ★★★★★     |
| 11      | Student Attendance       | Date range query, file export, custom exception                  | ★★★☆☆     |
| 12      | Employee Payroll         | Salary calc dict, experience years, file export                  | ★★★☆☆     |
| 13      | Hospital Appointment     | Time objects, dict grouping, slot conflict check                 | ★★★☆☆     |
| 14      | Inventory Restock        | Urgency grouping, UPDATE + rollback, append log file             | ★★★★☆     |
| 15      | Event Booking            | Two tables, INSERT + UPDATE transaction, nested dict             | ★★★★☆     |
| 16      | Crime Records            | Two tables, state validation, cross-referenced report            | ★★★★☆     |
| 17      | Subscription Service     | relativedelta renewal, 4-bucket expiry dict, GROUP BY revenue    | ★★★★☆     |
| 18      | Courier Tracking         | State machine transitions, CSV read + write, bulk processor      | ★★★★★     |
| 19      | Stock Portfolio          | Class-based, P/L metrics dict, sector grouping, DELETE/UPDATE    | ★★★★★     |
| 20      | Tournament Manager       | Class-based, points table calc, schedule conflict, bulk CSV load | ★★★★★     |

---

---

# PART A — Problems 1 to 10 (Foundation Series)

---

## Problem 1 – Student Management
**Table:** `student(student_id, name, department, year, marks)`

**Task:**
Write a function `retrieve_toppers_by_department(department, conn)` that:
- Fetches all students from the given **department** whose **marks >= 90**
- Returns a **list of Student objects** ordered by marks **descending**
- Returns an **empty list** if none found

**Sample Input:**
```
Enter the department: Computer Science
```
**Sample Output:**
```
Student ID: 101
Name: Ananya Sharma
Year: 3
Marks: 97
Student ID: 104
Name: Ravi Kumar
Year: 2
Marks: 92
```

---

## Problem 2 – Employee Management
**Table:** `employee(emp_id, name, designation, department, salary, joining_date)`

**Task:**
Write a function `retrieve_employees_by_salary_range(min_salary, max_salary, conn)` that:
- Fetches employees with **salary BETWEEN min_salary AND max_salary** (inclusive)
- Returns a **list of Employee objects** ordered by salary **ascending**
- Returns an **empty list** if none found

**Sample Input:**
```
Enter the minimum salary: 30000
Enter the maximum salary: 60000
```
**Sample Output:**
```
Emp ID: E201
Name: Kiran Mehta
Designation: Junior Developer
Department: IT
Salary: 35000.0
```

---

## Problem 3 – Product Management
**Table:** `product(product_id, product_name, category, price, stock_quantity, expiry_date)`

**Task:**
Write a function `retrieve_low_stock_products(category, threshold, conn)` that:
- Fetches products in the given **category** where **stock_quantity <= threshold** AND **expiry_date > today**
- Returns a **list of Product objects** ordered by **stock_quantity ascending**
- Returns an **empty list** if none found

**Sample Input:**
```
Enter the category: Dairy
Enter the stock threshold: 20
```
**Sample Output:**
```
Product ID: P301
Product Name: Fresh Milk
Price: 45.0
Stock Quantity: 10
Expiry Date: 2024-08-15
```

---

## Problem 4 – Order Management
**Table:** `orders(order_id, customer_name, product_id, quantity, order_date, status)`

**Task:**
Write two functions:
1. `place_order(order_obj, conn)` – Inserts the order into the DB. Returns `True` on success, `False` on failure.
2. `retrieve_orders_by_customer(customer_name, conn)` – Fetches all orders for the given customer. Returns list of Order objects ordered by **order_date descending**.

**Sample Input:**
```
Enter order ID: 5001
Enter customer name: Priya Nair
Enter product ID: 201
Enter quantity: 3
```
**Sample Output:**
```
Order placed successfully

--- Order History for Priya Nair ---
Order ID: 5001
Product ID: 201
Quantity: 3
Order Date: 2024-07-10
Status: Pending
```

---

## Problem 5 – Bank Account Management
**Table:** `bank_account(account_number, holder_name, account_type, balance, branch, ifsc_code)`

**Task:**
Write two functions:
1. `retrieve_account(account_number, conn)` – Returns a BankAccount object or `None` if not found.
2. `update_balance(account_number, amount, transaction_type, conn)` – Handles `deposit` or `withdraw`.
   - Deposit: add amount to balance
   - Withdraw: subtract only if `balance - amount >= 0`, else return `"Insufficient Balance"`
   - Invalid account: return `"Invalid Account"`
   - Success: commit and return `"Transaction Successful"`

**Sample Input:**
```
Enter account number: ACC10234
Enter amount: 5000
Enter transaction type (deposit/withdraw): withdraw
```
**Sample Output:**
```
Transaction Successful
Updated Balance: 12500.0
```

---

## Problem 6 – Doctor Management
**Table:** `doctor(doctor_id, name, specialization, hospital, experience_years, consultation_fee)`

**Task:**
Write a function `retrieve_doctors_by_specialization_and_experience(specialization, min_experience, conn)` that:
- Fetches doctors of the given **specialization** with **experience_years >= min_experience**
- Returns a **list of Doctor objects** ordered by **consultation_fee ascending**
- Returns an **empty list** if none found

**Sample Input:**
```
Enter the specialization: Cardiology
Enter minimum years of experience: 10
```
**Sample Output:**
```
Doctor ID: D501
Name: Dr. Suresh Patel
Hospital: Apollo
Experience: 15 years
Consultation Fee: 800.0
```

---

## Problem 7 – Library Management
**Table:** `book(book_id, title, author, genre, available_copies, issued_copies)`

**Task:**
Write two functions:
1. `retrieve_book_by_id(book_id, conn)` – Returns a Book object or `None`.
2. `issue_book(book_id, conn)` – Issues the book:
   - If book not found: return `"Invalid Book ID"`
   - If `available_copies == 0`: return `"No copies available"`
   - Else: decrement `available_copies` by 1, increment `issued_copies` by 1, commit, return `"Book Issued Successfully"`

**Sample Input:**
```
Enter the book ID: 701
```
**Sample Output:**
```
Book Issued Successfully
Title: The Alchemist
Author: Paulo Coelho
Remaining copies: 2
```

---

## Problem 8 – Vehicle Insurance Management
**Table:** `vehicle(vehicle_id, owner_name, vehicle_type, brand, model, registration_year, insurance_expiry)`

**Task:**
Write a function `retrieve_expired_insurance_vehicles(vehicle_type, conn)` that:
- Fetches all vehicles of the given **vehicle_type** where **insurance_expiry < today**
- Returns list of Vehicle objects ordered by **insurance_expiry ascending** (most overdue first)
- Returns empty list if none found
- Compute and print **days overdue** in the output section

**Valid vehicle types:** car, bike, truck, bus

**Sample Input:**
```
Enter the vehicle type: car
```
**Sample Output:**
```
Vehicle ID: V801
Owner: Ramesh Iyer
Brand: Maruti
Model: Swift
Days Overdue: 45
```

---

## Problem 9 – Exam Result Management *(Class-Based)*
**Table:** `exam_result(result_id, student_id, subject, exam_date, marks_obtained, max_marks, grade)`

**Task:**
Implement three methods inside the `ExamManagementSystem` class:

1. `retrieve_results_by_student(student_id)` – Returns list of ExamResult objects ordered by **exam_date descending**.
2. `calculate_percentage(student_id)` – Returns `(sum of marks_obtained / sum of max_marks) * 100` rounded to 2 decimal places. Returns `-1` if no results found.
3. `delete_result(result_id)` – Deletes a result by ID. Returns:
   - `"Result Not Found"` if ID doesn't exist
   - `"Result Deleted Successfully"` on success

**Sample Input:**
```
Enter student ID: 301
Enter result ID to delete (0 to skip): 9012
```
**Sample Output:**
```
Result ID: 9015
Subject: Mathematics
Marks: 88 / 100
Grade: A

Overall Percentage: 82.33%

Result Deleted Successfully
```

---

## Problem 10 – Vehicle Rental System *(Class-Based, Most Complex)*
**Table:** `rental(rental_id, customer_id, vehicle_id, start_date, end_date, daily_rate, total_amount, payment_status)`

**Task:**
Implement three methods inside the `RentalManagementSystem` class:

1. `create_rental(rental_id, customer_id, vehicle_id, start_date, end_date, daily_rate)`:
   - Calculate `total_amount = (end_date - start_date).days * daily_rate`
   - Set `payment_status = 'Pending'`
   - Insert into DB, commit, return Rental object
   - Return `None` if insertion fails

2. `retrieve_pending_rentals(customer_id)`:
   - Fetch all rentals for customer where `payment_status = 'Pending'`
   - Return list ordered by **start_date ascending**

3. `mark_as_paid(rental_id)`:
   - Return `"Invalid Rental ID"` if not found
   - Return `"Already Paid"` if already paid
   - Else update status to `'Paid'`, commit, return `"Payment Updated Successfully"`

**Sample Input:**
```
Enter rental ID: 1001
Enter customer ID: 55
Enter vehicle ID: 301
Enter start date: 2024-07-01
Enter end date: 2024-07-05
Enter daily rate: 1500
Enter rental ID to mark as paid: 1001
```
**Sample Output:**
```
Rental created. Total Amount: 6000.0

--- Pending Rentals ---
Rental ID: 1001
Vehicle ID: 301
Total Amount: 6000.0
Status: Pending

Payment Updated Successfully
```

---

---

# PART B — Problems 11 to 20 (Advanced Series)

> **Additional concepts covered:** Custom Exception Handling, Date/Time Manipulation,
> Collections (dict grouping, nested dicts, points tables), File Handling (read & write),
> Multi-table queries, Class-based systems with multiple interacting methods.

---

## Problem 11 – Student Attendance Management
**Tables:** `attendance(attendance_id, student_id, student_name, department, attendance_date, status)`

**Task:**
Write three functions in `attendance_management.py`:

1. `retrieve_attendance_by_date_range(department, from_date, to_date, conn)`
   - Fetches all attendance records for a department between from_date and to_date (inclusive)
   - Returns a **list of StudentAttendance objects** sorted by `attendance_date` ASC
   - Raises **`InvalidDepartmentException`** with message `"No records found for the given department and date range."` if no records found

2. `calculate_attendance_percentage(student_id, conn)`
   - Formula: `(Total Present / Total Records) * 100`, rounded to 2 decimal places
   - Returns **-1** if no records exist for that student_id

3. `export_to_file(attendance_list, filename)`
   - Writes each record as: `attendance_id,student_id,student_name,department,DD-MM-YYYY,status`
   - Raises **`IOError`** if file cannot be created

**Custom Exception:** `InvalidDepartmentException`

**Sample Input 1:**
```
Enter the department: Computer Science
Enter the from date (DD-MM-YYYY): 01-07-2024
Enter the to date (DD-MM-YYYY): 03-07-2024
```
**Sample Output 1:**
```
Attendance Records:
Student ID: 201
Student Name: Arun Kumar
Date: 01-07-2024
Status: Present
---
...

Enter student ID to calculate attendance percentage: 201
Attendance Percentage: 66.67%

Enter filename to export records (e.g. attendance.txt): cs_attendance.txt
Records exported successfully to cs_attendance.txt
```

**Sample Input 2:**
```
Enter the department: Mechanical
Enter the from date (DD-MM-YYYY): 01-07-2024
Enter the to date (DD-MM-YYYY): 03-07-2024
```
**Sample Output 2:**
```
No records found for the given department and date range.
```

**Sample Input 3:**
```
Enter the department: Computer Science
Enter the from date (DD-MM-YYYY): 2024/07/01
```
**Sample Output 3:**
```
Invalid date format. Please use DD-MM-YYYY.
```

---

## Problem 12 – Employee Payroll Management
**Table:** `employee(emp_id, emp_name, department, designation, basic_salary, joining_date)`

**Task:**
Write four functions in `payroll_management.py`:

1. `retrieve_employees_by_department(department, conn)`
   - Returns list of Employee objects sorted by `emp_id` ASC
   - Raises **`InvalidDepartmentException`** → `"No employees found in the given department."`

2. `calculate_net_salary(basic_salary)`
   - **Allowances:** HRA = 20%, DA = 15%, TA = 10% of basic
   - **Deductions:** PF = 12%, Tax = 10% (only if basic > 30000)
   - Returns a **dictionary** with keys: `hra`, `da`, `ta`, `pf`, `tax`, `gross_salary`, `net_salary`

3. `calculate_years_of_experience(joining_date)`
   - Returns number of complete years from joining_date to today
   - Raises **`InsufficientExperienceException`** → `"Employee has less than 1 year of experience."`

4. `export_payroll_report(employee_list, conn, filename)`
   - Writes formatted payroll report for each employee to a `.txt` file
   - Raises **`IOError`** if file cannot be written

**Custom Exceptions:** `InvalidDepartmentException`, `InsufficientExperienceException`

**Sample Input 1:**
```
Enter the department: IT
```
**Sample Output 1:**
```
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
...
Enter filename to export payroll report: it_payroll.txt
Payroll report exported successfully to it_payroll.txt
```

**Sample Input 2:**
```
Enter the department: Finance
```
**Sample Output 2 (basic <= 30000 → no tax):**
```
...
Tax        : 0.0
Net Salary : 37240.0
Experience : Employee has less than 1 year of experience.
```

**Sample Input 3:**
```
Enter the department: Marketing
```
**Sample Output 3:**
```
No employees found in the given department.
```

---

## Problem 13 – Hospital Appointment Management
**Table:** `appointment(appointment_id, patient_name, doctor_name, department, appointment_date, appointment_time, status)`

**Task:**
Write four functions in `appointment_management.py`:

1. `retrieve_appointments_by_doctor(doctor_name, conn)`
   - Returns list sorted by `appointment_date` ASC then `appointment_time` ASC
   - Raises **`InvalidDoctorException`** → `"No appointments found for the given doctor."`

2. `group_appointments_by_status(appointment_list)`
   - Returns a **dictionary**: `{'Scheduled': [...], 'Completed': [...], 'Cancelled': [...]}`
   - Raises **`InvalidStatusException`** → `"Invalid status found in records."` for unknown status

3. `check_slot_availability(doctor_name, appointment_date, appointment_time, conn)`
   - Returns `True` if slot is free
   - Raises **`AppointmentSlotConflictException`** → `"Slot already booked for the given doctor at this date and time."`

4. `export_appointments_to_file(appointment_list, filename)`
   - Each line: `appointment_id,patient_name,doctor_name,department,DD-MM-YYYY,HH:MM,status`
   - Raises **`IOError`** if file cannot be written

**Custom Exceptions:** `InvalidDoctorException`, `InvalidStatusException`, `AppointmentSlotConflictException`

**Sample Input 1:**
```
Enter the doctor name: Dr. Suresh Menon
```
**Sample Output 1:**
```
Appointment Summary for Dr. Dr. Suresh Menon
==================================================

[Scheduled] - 2 appointment(s)
  ID       : 1001
  Patient  : Ramesh Iyer
  Date     : 10-07-2024
  Time     : 09:00
  Dept     : Cardiology
...
Enter date to check slot availability (DD-MM-YYYY): 10-07-2024
Enter time to check (HH:MM, 24-hr): 09:00
Slot already booked for the given doctor at this date and time.
```

**Sample Input 2:**
```
Enter the doctor name: Dr. Nobody
```
**Sample Output 2:**
```
No appointments found for the given doctor.
```

---

## Problem 14 – Inventory Restock Management
**Table:** `product(product_id, product_name, category, quantity_in_stock, reorder_level, unit_price, last_restocked_date)`

**Task:**
Write five functions in `inventory_management.py`:

1. `retrieve_low_stock_products(category, conn)`
   - Fetches products where `quantity_in_stock <= reorder_level`, sorted by `quantity_in_stock` ASC
   - Raises **`InvalidCategoryException`** → `"No products found for the given category."` if category missing entirely
   - Raises **`RestockNotRequiredException`** → `"All products in this category are sufficiently stocked."` if category exists but none need restocking

2. `group_products_by_urgency(product_list)`
   - **Critical:** qty == 0 | **Low:** 0 < qty <= reorder//2 | **Moderate:** reorder//2 < qty <= reorder
   - Returns a **dictionary** with urgency levels as keys
   - Raises **`OutOfStockException`** → `"Critical stock alert: one or more products are completely out of stock."` **after** building the full dict

3. `calculate_days_since_restock(last_restocked_date)` – Returns `(today - last_restocked_date).days`

4. `restock_product(product_id, restock_quantity, conn)`
   - Updates stock + `last_restocked_date = today`. Commit. Rollback on error.
   - Returns `"Restock successful."` or raises **`InvalidCategoryException`** → `"Product ID not found."`

5. `write_restock_log(product_list, log_filename)`
   - **Appends** timestamped alert entries to a log file (creates if not exists)
   - Format: `[DD-MM-YYYY HH:MM] ALERT: <name> (ID: <id>) | Stock: <qty> | Reorder Level: <reorder> | Days Since Restock: <days>`

**Custom Exceptions:** `InvalidCategoryException`, `OutOfStockException`, `RestockNotRequiredException`

**Sample Input 1:**
```
Enter the product category: Electronics
```
**Sample Output 1:**
```
Warning: Critical stock alert: one or more products are completely out of stock.

Low Stock Report - Category: Electronics
=======================================================

[Critical]
  Product ID   : P101
  Name         : USB-C Cable
  Stock        : 0
  Reorder Level: 20
  Unit Price   : 299.0
  Days Since Restock: 127
...
Enter Product ID to restock: P101
Enter quantity to add: 50
Restock successful.
```

**Sample Input 2:**
```
Enter the product category: Grocery
```
**Sample Output 2:**
```
All products in this category are sufficiently stocked.
```

**Sample Input 3:**
```
Enter the product category: Furniture
```
**Sample Output 3:**
```
No products found for the given category.
```

---

## Problem 15 – Event Booking Management
**Tables:** `event(event_id, event_name, venue, event_date, event_time, total_seats, booked_seats, ticket_price)`, `booking(booking_id, event_id, customer_name, num_tickets, booking_date, total_amount)`

**Task:**
Write five functions in `event_management.py`:

1. `retrieve_event_by_id(event_id, conn)` – Returns Event object or raises **`EventNotFoundException`**

2. `retrieve_upcoming_events(conn)`
   - Fetches all events where `event_date >= today`, sorted by date then time
   - Raises **`EventNotFoundException`** → `"No upcoming events available."`

3. `book_tickets(event_id, customer_name, num_tickets, conn)`
   Validate in order: event exists → event not in past → num_tickets >= 1 → available seats >= num_tickets
   - `booking_id = event_id * 1000 + datetime.now().second`
   - INSERT booking + UPDATE event seats in **one transaction**; rollback on error
   - Returns **Booking object**

4. `get_seat_availability_summary(event_list)`
   - Returns a **nested dictionary** keyed by `event_id`:
     `{'event_name', 'total_seats', 'booked_seats', 'available_seats', 'occupancy_pct'}`

5. `export_booking_confirmation(booking_obj, event_obj, filename)`
   - Writes a formatted confirmation file (overwrite mode)

**Custom Exceptions:** `EventNotFoundException`, `EventExpiredException`, `SeatNotAvailableException`, `InvalidTicketCountException`

**Sample Input 1:**
```
Enter Event ID to book: 302
Enter your name: Kavya Nair
Enter number of tickets: 3
```
**Sample Output 1:**
```
Booking successful!
Booking ID  : 302045
Total Amount: Rs. 2400.0
```

**Sample Input 2:**
```
Enter Event ID to book: 303
Enter number of tickets: 1
```
**Sample Output 2:**
```
Not enough seats available. Only 0 seat(s) left.
```

**Sample Input 3:**
```
Enter Event ID to book: 305
```
**Sample Output 3:**
```
Cannot book tickets for a past event.
```

---

## Problem 16 – Crime Record Management System
**Tables:** `crime_record(record_id, case_number, crime_type, location, reported_date, status, officer_id, suspect_name)`, `officer(officer_id, officer_name, badge_number, rank, department, joining_date)`

**Valid crime types:** theft, assault, fraud, robbery, vandalism, murder

**Task:**
Write six functions in `crime_management.py`:

1. `retrieve_crimes_by_location(location, conn)` – Sorted by `reported_date` DESC. Raises **`InvalidLocationException`**

2. `retrieve_officer_details(officer_id, conn)` – Returns Officer object. Raises **`OfficerNotFoundException`**

3. `calculate_case_age_in_days(reported_date)` – Returns `(today - reported_date).days`

4. `update_case_status(record_id, new_status, conn)`
   Validate in order: record exists → not already Closed → new_status is valid
   - Returns `"Case status updated successfully."` on success

5. `group_crimes_by_type(crime_list)` – Returns dict with **title-cased** keys. Raises **`InvalidCrimeTypeException`** for unknown types

6. `export_crime_report(crime_list, conn, filename)` – Cross-referenced report calling `retrieve_officer_details()` per record. Writes `"Officer: Details not available"` if officer not found.

**Custom Exceptions:** `InvalidLocationException`, `InvalidCrimeTypeException`, `CaseAlreadyClosedException`, `OfficerNotFoundException`

**Sample Input 1:**
```
Enter the location to search crimes: Koramangala
```
**Sample Output 1:**
```
Crime Summary for Location: Koramangala
=======================================================
[Vandalism] - 1 case(s)
  Case No  : CR-2024-006
  Status   : Open
  Age      : 35 day(s)
...
Enter Crime Record ID to update status: 3
Enter new status: Open
Case is already closed and cannot be updated.
```

**Sample Input 2:**
```
Enter the location to search crimes: Whitefield
```
**Sample Output 2:**
```
No crime records found for the given location.
```

---

## Problem 17 – Subscription Service Management
**Table:** `subscription(subscription_id, customer_name, email, plan_type, start_date, end_date, monthly_fee, is_active)`

**Plan types and monthly fees:** Basic = Rs.199 | Standard = Rs.499 | Premium = Rs.999

**Task:**
Write six functions in `subscription_management.py`:

1. `retrieve_subscriptions_by_plan(plan_type, conn)` – Sorted by `end_date` ASC. Raises **`InvalidPlanTypeException`** or **`SubscriptionNotFoundException`**

2. `get_expiry_status(end_date)` – Returns: `'Expired'` (< 0 days) | `'Expires Today'` (0) | `'Expiring Soon'` (1–7) | `'Active'` (> 7)

3. `group_subscriptions_by_expiry_status(subscription_list)` – Groups into 4-bucket dictionary

4. `renew_subscription(subscription_id, renewal_months, conn)`
   Validate: exists → is_active == 1 → 1 <= months <= 12
   - `new_end_date = end_date + relativedelta(months=renewal_months)`
   - Returns tuple `(new_end_date, total_cost)`

5. `calculate_total_revenue_by_plan(conn)` – `GROUP BY` on active subs. Returns dict with all 3 plans (0.0 if none active)

6. `export_expiry_alert_report(subscription_list, filename)` – Writes **only** Expired/Expiring Soon/Expires Today subs. Writes `"No subscriptions requiring alerts."` if all Active.

**Custom Exceptions:** `InvalidPlanTypeException`, `SubscriptionNotFoundException`, `SubscriptionInactiveException`

> 💡 Requires: `pip install python-dateutil`

**Sample Input 1:**
```
Enter the plan type (Basic / Standard / Premium): Basic
```
**Sample Output 1:**
```
[Expired] - 1 subscription(s)
  ID       : 1001
  Customer : Arjun Mehta
  End Date : 25-07-2024
  Days     : -11
...
Monthly Revenue by Plan (Active Subscriptions):
  Basic       : Rs. 597.0
  Standard    : Rs. 998.0
  Premium     : Rs. 999.0

Enter Subscription ID to renew: 1001
Enter number of months to renew (1-12): 3
Renewal successful!
New End Date     : 25-10-2024
Renewal Cost     : Rs. 597.0
```

**Sample Input 2:**
```
Enter the plan type: Gold
```
**Sample Output 2:**
```
Invalid plan type. Choose from Basic, Standard, or Premium.
```

---

## Problem 18 – Courier Tracking System
**Tables:** `shipment(shipment_id, tracking_number, sender_name, receiver_name, origin_city, destination_city, dispatch_date, expected_delivery_date, weight_kg, status)`, `tracking_event(event_id, shipment_id, event_datetime, location, event_description)`

**Status pipeline:** Booked → In Transit → Out for Delivery → Delivered | Returned

**Task:**
Write six functions in `courier_management.py`:

1. `retrieve_shipment_by_tracking(tracking_number, conn)` – Raises **`ShipmentNotFoundException`**

2. `retrieve_tracking_history(shipment_id, conn)` – Returns list sorted by `event_datetime` ASC. Returns **empty list** (no exception) if no events yet.

3. `calculate_delivery_metrics(shipment_obj)` – Returns dict: `days_in_transit`, `days_until_due`, `is_overdue`, `shipping_cost`
   - Shipping cost tiers: ≤5kg × Rs.50 | 5–20kg × Rs.40 | >20kg × Rs.30

4. `update_shipment_status(tracking_number, new_status, location, description, conn)`
   Validate: exists → not terminal → valid transition
   - INSERT tracking_event + UPDATE shipment in **one transaction**; rollback on error

5. `load_bulk_status_updates_from_file(filepath, conn)` – Reads CSV `(tracking_number, new_status, location, description)`. **Never stops on failure.** Returns list of `(tracking_number, 'SUCCESS'/'FAILED', message)` tuples.

6. `export_shipment_report(shipment_obj, tracking_history, metrics, filename)` – Full formatted report with tracking history

**Custom Exceptions:** `ShipmentNotFoundException`, `InvalidStatusTransitionException`, `DeliveredShipmentException`, `TrackingFileReadException`

**Sample Input 1:**
```
Enter tracking number: TRK-1001
```
**Sample Output 1:**
```
Shipment Found: TRK-1001
Status         : In Transit
Route          : Mumbai -> Bangalore
Days In Transit: 4
Days Until Due : 0
Overdue        : No
Shipping Cost  : Rs. 175.0
...
Enter new status to update: Out for Delivery
Status updated to Out for Delivery.
```

**Sample Input 2:**
```
Enter tracking number: TRK-1001
Enter new status: Delivered
Invalid transition: In Transit -> Delivered
```

---

## Problem 19 – Stock Portfolio Management System *(Class-Based)*
**Tables:** `stock(stock_id, symbol, company_name, sector, current_price, listed_date)`, `portfolio(portfolio_id, investor_name, stock_id, symbol, quantity, buy_price, buy_date)`

**Valid sectors:** IT, Banking, Pharma, Energy, FMCG, Auto

**Task:**
Implement eight methods inside the `StockPortfolioSystem` class:

1. `retrieve_portfolio_by_investor(investor_name)` – List sorted by `buy_date` ASC. Raises **`InvestorNotFoundException`**
2. `retrieve_stock_by_symbol(symbol)` – Returns Stock object. Raises **`StockNotFoundException`**
3. `calculate_holding_metrics(portfolio_obj)` – Returns dict: `invested_value`, `current_value`, `profit_loss`, `profit_loss_pct`, `holding_days`, plus symbol/company/sector/qty/prices
4. `group_portfolio_by_sector(portfolio_list)` – Groups into title-cased sector dict. Raises **`InvalidSectorException`**
5. `add_holding(investor_name, symbol, quantity, buy_price, buy_date_str)` – Validate: stock exists → no duplicate → qty ≥ 1 → price > 0. INSERT + commit.
6. `sell_holding(investor_name, symbol, sell_quantity, conn)` – Validate: stock exists → holding exists → sufficient qty. DELETE (full exit) or UPDATE (partial).
7. `get_portfolio_summary(investor_name)` – Aggregates all holdings. Returns dict with `total_invested`, `total_current`, `total_pl`, `overall_pl_pct`, `best_performer`, `worst_performer`
8. `export_portfolio_report(summary_dict, sector_groups, filename)` – Multi-section report: holdings table + sector breakdown + summary block

**Custom Exceptions:** `InvestorNotFoundException`, `StockNotFoundException`, `InsufficientSharesException`, `InvalidSectorException`, `DuplicateHoldingException`

**Sample Input 1 (View portfolio):**
```
Enter choice (1/2/3): 1
Enter investor name: Arjun Mehta
```
**Sample Output 1:**
```
INFY     | Qty: 50  | Buy: 1500.0 | Now: 1850.0 | P/L: +17500.0 (+23.33%) | Days: 207
HDFCBK   | Qty: 30  | Buy: 1580.0 | Now: 1620.0 | P/L: +1200.0  (+2.53%)  | Days: 171

  Total Invested  : Rs. 188400.0
  Best Performer  : INFY
  Worst Performer : HDFCBK
```

**Sample Input 2 (Duplicate holding):**
```
Enter choice: 2 | Symbol: INFY
```
**Sample Output 2:**
```
Investor already holds INFY. Use sell to modify.
```

**Sample Input 3 (Oversell):**
```
Enter choice: 3 | Symbol: RELIND | Qty: 50
```
**Sample Output 3:**
```
Cannot sell 50 shares. Only 20 held.
```

---

## Problem 20 – Tournament Management System *(Class-Based, Most Complex)*
**Tables:** `team(team_id, team_name, city, coach_name, group_name, registration_date)`, `match_schedule(match_id, team1_id, team2_id, match_date, venue, team1_score, team2_score, status, stage)`

> ⚠️ Table is named `match_schedule` (not `match`) — `MATCH` is a reserved word in Oracle SQL.

**Constants:** Groups: A/B/C/D | Stages: Group, Quarter Final, Semi Final, Final | Win=3pts, Draw=1pt, Loss=0pts

**Task:**
Implement ten methods (including one private helper) inside the `TournamentManager` class:

1. `retrieve_teams_by_group(group_name)` – Raises **`InvalidGroupException`** (bad group) or **`TeamNotFoundException`** (empty group)
2. `retrieve_match_by_id(match_id)` – Raises **`MatchNotFoundException`**
3. `retrieve_matches_by_stage(stage)` – Raises if invalid stage; returns **empty list** if valid but no matches
4. `record_match_result(match_id, team1_score, team2_score)` – Validate: exists → not Completed/Cancelled → scores ≥ 0. UPDATE + commit. Returns `"Team1 wins."` / `"Team2 wins."` / `"Draw."`
5. `compute_group_standings(group_name)` – Builds points table from completed matches. Returns list of dicts sorted by points DESC then goal_difference DESC with rank.
6. `schedule_match(team1_id, team2_id, match_date_str, venue, stage)` – Validate: stage valid → both teams exist → date parseable → no schedule conflict. INSERT + commit.
7. `group_matches_by_stage(match_list)` – Groups Match objects by stage into dict
8. `load_results_from_file(filepath)` – Reads CSV `match_id,team1_score,team2_score`. Never stops on failure. Returns list of `(match_id, 'SUCCESS'/'FAILED', msg)`.
9. `_get_team_name_by_id(team_id)` – Private helper. Returns team_name or `'Unknown'`
10. `export_tournament_report(filename)` – Master method: all group standings + all stage matches (with team names) + tournament stats. Handles missing groups gracefully.

**Custom Exceptions:** `TeamNotFoundException`, `MatchNotFoundException`, `InvalidGroupException`, `MatchAlreadyCompletedException`, `InvalidScoreException`, `ScheduleConflictException`

**Sample Input 1 (View standings):**
```
Enter choice (1-5): 1
Enter group (A/B/C/D): A
```
**Sample Output 1:**
```
=== Group A Standings ===
Rank  Team                 P    W    D    L    GF   GA   GD    Pts
1     Warriors FC          2    2    0    0    5    1    +4    6
2     Storm City           2    1    0    1    3    2    +1    3
3     Thunder United       2    0    0    2    1    6    -5    0
```

**Sample Input 2 (Already completed):**
```
Enter match ID: 101 | Score: 2-0
```
**Sample Output 2:**
```
Match 101 is already Completed.
```

**Sample Input 3 (Schedule conflict):**
```
Team1 ID: 1 | Date: 10-08-2024
```
**Sample Output 3:**
```
Team Warriors FC already has a match scheduled on 10-08-2024.
```

**Sample Input 4 (Bulk load):**
```
Enter path to results CSV file: match_results.csv
```
**Sample Output 4:**
```
Match 101 -> [SUCCESS] Team1 wins.
Match 102 -> [SUCCESS] Draw.
Match 105 -> [FAILED] Match 105 is already Completed.
```

---

---

# SQL Table Creation Scripts (Oracle)

```sql
-- ── PART A (Problems 1–10) ─────────────────────────────────────────────────

-- Problem 1
CREATE TABLE student (
    student_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    department VARCHAR2(100),
    year NUMBER,
    marks NUMBER
);

-- Problem 2
CREATE TABLE employee (
    emp_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100),
    designation VARCHAR2(100),
    department VARCHAR2(100),
    salary NUMBER(10,2),
    joining_date DATE
);

-- Problem 3
CREATE TABLE product (
    product_id VARCHAR2(20) PRIMARY KEY,
    product_name VARCHAR2(100),
    category VARCHAR2(50),
    price NUMBER(10,2),
    stock_quantity NUMBER,
    expiry_date DATE
);

-- Problem 4
CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    customer_name VARCHAR2(100),
    product_id NUMBER,
    quantity NUMBER,
    order_date DATE,
    status VARCHAR2(20)
);

-- Problem 5
CREATE TABLE bank_account (
    account_number VARCHAR2(20) PRIMARY KEY,
    holder_name VARCHAR2(100),
    account_type VARCHAR2(20),
    balance NUMBER(12,2),
    branch VARCHAR2(100),
    ifsc_code VARCHAR2(20)
);

-- Problem 6
CREATE TABLE doctor (
    doctor_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100),
    specialization VARCHAR2(100),
    hospital VARCHAR2(100),
    experience_years NUMBER,
    consultation_fee NUMBER(10,2)
);

-- Problem 7
CREATE TABLE book (
    book_id NUMBER PRIMARY KEY,
    title VARCHAR2(200),
    author VARCHAR2(100),
    genre VARCHAR2(50),
    available_copies NUMBER,
    issued_copies NUMBER
);

-- Problem 8
CREATE TABLE vehicle (
    vehicle_id VARCHAR2(20) PRIMARY KEY,
    owner_name VARCHAR2(100),
    vehicle_type VARCHAR2(20),
    brand VARCHAR2(50),
    model VARCHAR2(50),
    registration_year NUMBER,
    insurance_expiry DATE
);

-- Problem 9
CREATE TABLE exam_result (
    result_id NUMBER PRIMARY KEY,
    student_id NUMBER,
    subject VARCHAR2(100),
    exam_date DATE,
    marks_obtained NUMBER,
    max_marks NUMBER,
    grade VARCHAR2(5)
);

-- Problem 10
CREATE TABLE rental (
    rental_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    vehicle_id NUMBER,
    start_date DATE,
    end_date DATE,
    daily_rate NUMBER(10,2),
    total_amount NUMBER(10,2),
    payment_status VARCHAR2(20)
);


-- ── PART B (Problems 11–20) ────────────────────────────────────────────────

-- Problem 11
CREATE TABLE attendance (
    attendance_id    NUMBER PRIMARY KEY,
    student_id       NUMBER,
    student_name     VARCHAR2(100),
    department       VARCHAR2(100),
    attendance_date  DATE,
    status           VARCHAR2(10)   -- 'Present' or 'Absent'
);

-- Problem 12
CREATE TABLE employee (
    emp_id        NUMBER PRIMARY KEY,
    emp_name      VARCHAR2(100),
    department    VARCHAR2(100),
    designation   VARCHAR2(100),
    basic_salary  NUMBER(10,2),
    joining_date  DATE
);

-- Problem 13
CREATE TABLE appointment (
    appointment_id   NUMBER PRIMARY KEY,
    patient_name     VARCHAR2(100),
    doctor_name      VARCHAR2(100),
    department       VARCHAR2(100),
    appointment_date DATE,
    appointment_time VARCHAR2(5),   -- stored as 'HH:MM'
    status           VARCHAR2(20)   -- 'Scheduled', 'Completed', 'Cancelled'
);

-- Problem 14
CREATE TABLE product (
    product_id           VARCHAR2(10) PRIMARY KEY,
    product_name         VARCHAR2(100),
    category             VARCHAR2(50),
    quantity_in_stock    NUMBER,
    reorder_level        NUMBER,
    unit_price           NUMBER(10,2),
    last_restocked_date  DATE
);

-- Problem 15
CREATE TABLE event (
    event_id      NUMBER PRIMARY KEY,
    event_name    VARCHAR2(100),
    venue         VARCHAR2(100),
    event_date    DATE,
    event_time    VARCHAR2(5),
    total_seats   NUMBER,
    booked_seats  NUMBER,
    ticket_price  NUMBER(10,2)
);

CREATE TABLE booking (
    booking_id    NUMBER PRIMARY KEY,
    event_id      NUMBER,
    customer_name VARCHAR2(100),
    num_tickets   NUMBER,
    booking_date  DATE,
    total_amount  NUMBER(10,2)
);

-- Problem 16
CREATE TABLE crime_record (
    record_id     NUMBER PRIMARY KEY,
    case_number   VARCHAR2(20),
    crime_type    VARCHAR2(30),
    location      VARCHAR2(100),
    reported_date DATE,
    status        VARCHAR2(30),
    officer_id    NUMBER,
    suspect_name  VARCHAR2(100)
);

CREATE TABLE officer (
    officer_id    NUMBER PRIMARY KEY,
    officer_name  VARCHAR2(100),
    badge_number  VARCHAR2(20),
    rank          VARCHAR2(50),
    department    VARCHAR2(100),
    joining_date  DATE
);

-- Problem 17
CREATE TABLE subscription (
    subscription_id  NUMBER PRIMARY KEY,
    customer_name    VARCHAR2(100),
    email            VARCHAR2(100),
    plan_type        VARCHAR2(20),
    start_date       DATE,
    end_date         DATE,
    monthly_fee      NUMBER(8,2),
    is_active        NUMBER(1)       -- 1 = Active, 0 = Inactive
);

-- Problem 18
CREATE TABLE shipment (
    shipment_id             NUMBER PRIMARY KEY,
    tracking_number         VARCHAR2(20) UNIQUE,
    sender_name             VARCHAR2(100),
    receiver_name           VARCHAR2(100),
    origin_city             VARCHAR2(100),
    destination_city        VARCHAR2(100),
    dispatch_date           DATE,
    expected_delivery_date  DATE,
    weight_kg               NUMBER(8,2),
    status                  VARCHAR2(30)
);

CREATE TABLE tracking_event (
    event_id          NUMBER PRIMARY KEY,
    shipment_id       NUMBER,
    event_datetime    TIMESTAMP,
    location          VARCHAR2(100),
    event_description VARCHAR2(300)
);

-- Problem 19
CREATE TABLE stock (
    stock_id       NUMBER PRIMARY KEY,
    symbol         VARCHAR2(10) UNIQUE,
    company_name   VARCHAR2(100),
    sector         VARCHAR2(30),
    current_price  NUMBER(10,2),
    listed_date    DATE
);

CREATE TABLE portfolio (
    portfolio_id   NUMBER PRIMARY KEY,
    investor_name  VARCHAR2(100),
    stock_id       NUMBER,
    symbol         VARCHAR2(10),
    quantity       NUMBER,
    buy_price      NUMBER(10,2),
    buy_date       DATE
);

-- Problem 20
CREATE TABLE team (
    team_id           NUMBER PRIMARY KEY,
    team_name         VARCHAR2(100),
    city              VARCHAR2(100),
    coach_name        VARCHAR2(100),
    group_name        VARCHAR2(2),
    registration_date DATE
);

CREATE TABLE match_schedule (
    match_id     NUMBER PRIMARY KEY,
    team1_id     NUMBER,
    team2_id     NUMBER,
    match_date   DATE,
    venue        VARCHAR2(100),
    team1_score  NUMBER,
    team2_score  NUMBER,
    status       VARCHAR2(20),
    stage        VARCHAR2(20)
);
```
