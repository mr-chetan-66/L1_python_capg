============================================================
  LIBRARY BOOK LENDING FINE CALCULATOR — PRACTICE PROBLEM
============================================================

PROBLEM STATEMENT
-----------------
A public library tracks book lending records. Your task is to build a
system that reads lending data from a file, calculates charges based on
membership type, stores records in an Oracle database, supports lookup
by lending ID, and applies fine increments for heavy borrowers.

------------------------------------------------------------
DATABASE TABLE  (run this DDL before executing your program)
------------------------------------------------------------

CREATE TABLE book_lending (
    lending_id       VARCHAR2(10)   PRIMARY KEY,
    student_id       VARCHAR2(10),
    date_of_lending  DATE,
    membership_type  VARCHAR2(10),
    due_date         DATE,
    no_of_books      NUMBER,
    late_days        NUMBER,
    payment_status   VARCHAR2(10),
    base_charge      NUMBER(10,2),
    late_fine        NUMBER(10,2),
    discount         NUMBER(10,2),
    net_amount       NUMBER(10,2)
);

------------------------------------------------------------
INPUT FILE FORMAT  (input.txt — comma-separated)
------------------------------------------------------------

  lending_id, student_id, date_of_lending, membership_type,
  due_date, no_of_books, late_days, payment_status

------------------------------------------------------------
CHARGE CALCULATION RULES
------------------------------------------------------------

  Membership | Base Charge/Book | Late Fine/Day | Discount Rate
  -----------+------------------+---------------+--------------
  Gold       |    500.0         |    50.0       |    15 %
  Silver     |    300.0         |   100.0       |    10 %
  Bronze     |    150.0         |   150.0       |     0 %

  base_charge  = charge_per_book  × no_of_books
  late_fine    = fine_per_day     × late_days
  discount     = base_charge      × (discount_rate / 100)
  net_amount   = base_charge + late_fine - discount

------------------------------------------------------------
FILTER RULES  (utility.read_file)
------------------------------------------------------------

  Include a record ONLY if BOTH conditions hold:
    1. payment_status == "Paid"
    2. (due_date - date_of_lending).days <= 365

------------------------------------------------------------
LENDING ID VALIDATION  (utility.validate_lending_id)
------------------------------------------------------------

  Pattern : starts with 'L' (uppercase) followed by exactly 3 digits
  Examples : L001, L012, L999   →  valid
             L00A, l001, L1234  →  invalid
  Behavior :
    • Return True  if valid
    • Raise InvalidLendingIdException("Invalid Lending Id") if invalid,
      catch it inside the same function, and return the message string

------------------------------------------------------------
UPDATE FINES  (book_lending_service.update_fines)
------------------------------------------------------------

  For every record where no_of_books > min_books:
    • Increase late_fine  by 12%  (multiply by 112/100)
    • Increase net_amount by 12%  (multiply by 112/100)
  Commit, then fetch and return the updated objects.

------------------------------------------------------------
EXPECTED PROGRAM FLOW  (main.py)
------------------------------------------------------------

  1. Load records from input.txt → insert into DB.
  2. Prompt: "Enter the Lending Id: "
       - If valid and found   → display the record
       - If valid but missing → "No record found"
       - If invalid           → print exception message
  3. Prompt: "Enter the minimum number of books for fine increment: "
       - If records updated → display each updated record
       - If none updated    → "No Records Updated"

------------------------------------------------------------
FILES YOU MUST COMPLETE
------------------------------------------------------------

  exception.py           → InvalidLendingIdException constructor + get_message()
  utility.py             → validate_lending_id(), read_file()
  book_lending_service.py→ ALL methods marked "Write your code here"
  main.py                → ALL steps marked "Write your code here"

  book_lending.py        → Already complete. Do NOT modify.

------------------------------------------------------------
DISPLAY FORMAT  (implemented for you in main.py)
------------------------------------------------------------

  Lending Id        : L001
  Student Id        : S101
  Membership Type   : Gold
  Due Date          : 2023-06-10
  No. of Books      : 5
  Late Days         : 3
  Base Charge       : 2500.00
  Late Fine         : 150.00
  Discount          : 375.00
  Net Amount        : 2275.00

============================================================
