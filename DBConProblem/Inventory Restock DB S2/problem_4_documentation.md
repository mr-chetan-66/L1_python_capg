# Problem 4 — Inventory Restock Management System

## Overview

A **single-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers a two-step SELECT (COUNT then filtered query), urgency-bucketed dictionary grouping with a post-build exception, days-since-restock calculation, UPDATE with rollback, and append-mode timestamped log file writing.

---

## File Structure

```
problem_4_inventory/
│
├── database.properties      → DB credentials config
├── product.py               → Entity class (7 fields, getters & setters)
├── exceptions.py            → 3 custom exception classes
├── product_dao.py           → Class-based DAO (2 DB methods: SELECT + UPDATE)
├── inventory_util.py        → Utility helpers (urgency grouping, days calc, display, log write)
└── main.py                  → Entry point (3-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `product.py` | Entity class — 7 fields, getters & setters |
| `exceptions.py` | 3 custom exceptions isolated in one place |
| `product_dao.py` | Class-based DAO — 2 methods: two-step SELECT for low stock, UPDATE for restock with rollback |
| `inventory_util.py` | Helpers — urgency grouping (raises after build), silent rebuild helper, days calc, display, append-mode log write |
| `main.py` | Entry point — 3-step flow: retrieve + group → write log → restock product |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT COUNT + SELECT** | `retrieve_low_stock_products()` | Two queries: COUNT first to distinguish "no category" from "all stocked"; then filter `qty <= reorder_level` sorted ASC |
| **UPDATE** | `restock_product()` | Checks product exists first; updates both `quantity_in_stock` and `last_restocked_date`; `conn.rollback()` on `cx_Oracle.DatabaseError` |

---

## Oracle Table

```sql
CREATE TABLE product (
    product_id           VARCHAR2(10) PRIMARY KEY,
    product_name         VARCHAR2(100),
    category             VARCHAR2(50),
    quantity_in_stock    NUMBER,
    reorder_level        NUMBER,
    unit_price           NUMBER(10, 2),
    last_restocked_date  DATE
);
```

---

## Entity Class — `product.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | VARCHAR2(10) | Primary key (e.g. `P101`) |
| `product_name` | VARCHAR2(100) | Name of the product |
| `category` | VARCHAR2(50) | Product category |
| `quantity_in_stock` | NUMBER | Current stock quantity |
| `reorder_level` | NUMBER | Minimum stock — restock if `qty <= this` |
| `unit_price` | NUMBER(10,2) | Price per unit |
| `last_restocked_date` | DATE | Date the product was last restocked |

All fields are **private** with public getters and setters following encapsulation principles.

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `InvalidCategoryException` | Category not found in DB; OR product_id not found during restock |
| `OutOfStockException` | Any product has `quantity_in_stock == 0` — raised **after** building the grouped dict |
| `RestockNotRequiredException` | Category exists but all products are above their reorder level |

---

## DAO Class — `product_dao.py`

```python
class ProductDao:
    def __init__(self, conn): ...
```

### Methods

#### `retrieve_low_stock_products(category)`
- **Step 1:** `SELECT COUNT(*)` to check if category exists at all
  - Count == 0 → raises `InvalidCategoryException`
- **Step 2:** `SELECT ... WHERE qty <= reorder_level ORDER BY qty ASC`
  - No rows → raises `RestockNotRequiredException`
- Safely converts Oracle DATE → `date` using `hasattr(..., 'date')`
- Returns list of `Product` objects sorted most critical first

#### `restock_product(product_id, restock_quantity)`
- `SELECT COUNT(*)` to confirm product exists → raises `InvalidCategoryException` if not
- `UPDATE` sets `quantity_in_stock = quantity_in_stock + restock_quantity` and `last_restocked_date = date.today()`
- Commits, calls `conn.rollback()` on `cx_Oracle.DatabaseError`
- Returns `"Restock successful."`

---

## Utility Functions — `inventory_util.py`

| Function | Description |
|----------|-------------|
| `group_products_by_urgency(product_list)` | Returns `{urgency: [Product, ...]}` dict; raises `OutOfStockException` **after** building if any `qty == 0` |
| `build_urgency_groups_silent(product_list)` | Same grouping logic but **never raises** — used by `main.py` after catching `OutOfStockException` to recover the grouped dict |
| `calculate_days_since_restock(last_restocked_date)` | Returns `(date.today() - last_restocked_date).days` as int |
| `display_low_stock_report(category, urgency_groups)` | Prints urgency-grouped stock report with days since restock per product |
| `write_restock_log(product_list, log_filename)` | Appends timestamped `ALERT:` entries; uses `'a'` mode — creates file if not exists; raises `IOError` on failure |

### Urgency Grouping Rules

| Key | Condition |
|-----|-----------|
| `'Critical'` | `quantity_in_stock == 0` |
| `'Low'` | `0 < quantity_in_stock <= reorder_level // 2` |
| `'Moderate'` | `reorder_level // 2 < quantity_in_stock <= reorder_level` |

Only keys with at least one product appear in the returned dictionary.

---

## The OutOfStockException Pattern — Key Design Point

`group_products_by_urgency` is specified to **build the full dict first, then raise**.
This means the dict is lost when the exception propagates to the caller.

`main.py` handles this with a two-step pattern:

```python
urgency_groups = {}
try:
    urgency_groups = util.group_products_by_urgency(low_stock_products)
except OutOfStockException as e:
    print(f"Warning: {e}")
    # Recover the grouped dict using the silent helper
    urgency_groups = util.build_urgency_groups_silent(low_stock_products)
```

`build_urgency_groups_silent()` in `inventory_util.py` is the dedicated clean recovery function — same logic, no exception.

---

## Main Program Flow — `main.py`

```
Step 1 — LOW STOCK REPORT
    ├── Input: category
    ├── Call: product_dao.retrieve_low_stock_products(category)
    ├── Call: util.group_products_by_urgency(low_stock_products)
    │         → catch OutOfStockException, print warning, rebuild silently
    └── Display: util.display_low_stock_report(category, urgency_groups)

Step 2 — WRITE RESTOCK LOG
    ├── Input: log_filename
    ├── Call: util.write_restock_log(low_stock_products, log_filename)
    └── Display: confirmation message

Step 3 — RESTOCK A PRODUCT
    ├── Input: product_id, restock_quantity
    ├── Call: product_dao.restock_product(product_id, restock_quantity)
    └── Display: result message
```

---

## Sample Run

```
=======================================================
       INVENTORY RESTOCK MANAGEMENT SYSTEM
=======================================================

--- LOW STOCK REPORT ---
Enter Product Category : Electronics
Warning: Critical stock alert: one or more products are completely out of stock.

Low Stock Report - Category: Electronics
=======================================================

[Critical]
  Product ID        : P101
  Name              : USB-C Cable
  Stock             : 0
  Reorder Level     : 20
  Unit Price        : 299.0
  Days Since Restock: 127

[Low]
  Product ID        : P102
  Name              : Wireless Mouse
  Stock             : 8
  Reorder Level     : 20
  Unit Price        : 899.0
  Days Since Restock: 81

[Moderate]
  Product ID        : P103
  Name              : HDMI Adapter
  Stock             : 14
  Reorder Level     : 20
  Unit Price        : 499.0
  Days Since Restock: 56

--- WRITE RESTOCK LOG ---
Enter Log Filename to Write Restock Alerts : restock_log.txt
Restock log written to restock_log.txt

--- RESTOCK A PRODUCT ---
Enter Product ID to Restock   : P101
Enter Quantity to Add          : 50
Restock successful.
```

---

## Sample Log File Entry (restock_log.txt)

```
[05-08-2024 14:32] ALERT: USB-C Cable (ID: P101) | Stock: 0 | Reorder Level: 20 | Days Since Restock: 127
[05-08-2024 14:32] ALERT: Wireless Mouse (ID: P102) | Stock: 8 | Reorder Level: 20 | Days Since Restock: 81
[05-08-2024 14:32] ALERT: HDMI Adapter (ID: P103) | Stock: 14 | Reorder Level: 20 | Days Since Restock: 56
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Category not in DB at all | `InvalidCategoryException` — "No products found for the given category." |
| Category exists but all products stocked | `RestockNotRequiredException` — "All products in this category are sufficiently stocked." |
| Any product has `qty == 0` | `OutOfStockException` warning printed; grouped dict rebuilt silently; report shown in full |
| Product ID not found during restock | `InvalidCategoryException` — "Product ID not found." |
| DB error during UPDATE | `conn.rollback()` called; `cx_Oracle.DatabaseError` re-raised |
| Log file write fails | `IOError` raised from `write_restock_log` |
| Non-numeric restock quantity | `ValueError` caught in `main()` |

---

## Key Python Concepts Used

```python
# Two-step SELECT: COUNT first, then filtered query
SELECT COUNT(*) FROM product WHERE LOWER(category) = :1
SELECT ... WHERE LOWER(category) = :1 AND quantity_in_stock <= reorder_level

# Urgency bucketing with integer division
if qty == 0:             urgency = 'Critical'
elif qty <= reorder // 2: urgency = 'Low'
else:                    urgency = 'Moderate'

# Raise AFTER building the dict — spec requirement
if has_critical:
    raise OutOfStockException("Critical stock alert: ...")
return grouped          # never reached if Critical exists

# Append-mode log file — creates if not exists
with open(log_filename, 'a') as f: ...

# Timestamped log entry
now = datetime.now().strftime("%d-%m-%Y %H:%M")

# UPDATE two columns in one statement
UPDATE product
SET quantity_in_stock   = quantity_in_stock + :1,
    last_restocked_date = :2
WHERE product_id = :3
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Payroll | SELECT + salary dict + experience calc + file report |
| 3 | Hospital Appointment | SELECT + COUNT slot check + dict grouping + CSV export |
| **4** | **Inventory Restock** | **Two-step SELECT + urgency dict + post-build exception + UPDATE + append log** |
| 5 | Event Booking | Two-table DAO + 4-step validation + INSERT+UPDATE transaction + nested dict |
| 6 | Crime Record Management | Two-table DAO + Custom Exceptions + Dict Grouping + File Report |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
