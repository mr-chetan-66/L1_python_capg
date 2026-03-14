# Problem 3 — Product Low Stock Finder

## Overview

A Python + Oracle Database problem focused on **multi-condition WHERE filtering** including a **SYSDATE date comparison** to exclude expired products. Also introduces **Python-side date arithmetic** to calculate days remaining until expiry.

---

## File Structure

```
problem_3_product/
│
├── database.properties    → DB credentials config
├── product.py             → Entity class (6 fields, getters & setters)
├── product_dao.py         → DAO (1 DB function)
├── product_util.py        → Utility helpers (validation, display, date calc)
└── main.py                → Entry point (search and display flow)
```

---

## Oracle Table

```sql
CREATE TABLE product (
    product_id     VARCHAR2(20) PRIMARY KEY,
    product_name   VARCHAR2(100),
    category       VARCHAR2(50),
    price          NUMBER(10,2),
    stock_quantity NUMBER,
    expiry_date    DATE
);
```

---

## Entity Class — `product.py`

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | VARCHAR2(20) | Primary key |
| `product_name` | VARCHAR2(100) | Name of the product |
| `category` | VARCHAR2(50) | Product category |
| `price` | NUMBER(10,2) | Price per unit |
| `stock_quantity` | NUMBER | Units currently in stock |
| `expiry_date` | DATE | Product expiry date |

All fields are **private** with public getters and setters.

---

## DAO Function — `product_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_low_stock_products(category, threshold, conn)` | SELECT | Fetch products in given category where stock <= threshold AND expiry is in the future, ordered by stock ASC |

### Key SQL — Multi-Condition Filter

```sql
SELECT product_id, product_name, category, price, stock_quantity, expiry_date
FROM product
WHERE LOWER(category) = LOWER(:1)
  AND stock_quantity <= :2
  AND expiry_date > SYSDATE
ORDER BY stock_quantity ASC
```

> **Note:** `SYSDATE` is Oracle's built-in function for the current date and time. `expiry_date > SYSDATE` ensures only non-expired products are returned.

---

## Utility Functions — `product_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_category(category)` | Returns `True` if category is in the valid list |
| `is_valid_threshold(threshold)` | Returns `True` only if threshold > 0 |
| `display_product(product)` | Prints all product fields neatly |
| `get_result_count(list)` | Returns length of product list |
| `get_days_until_expiry(product)` | Returns `(expiry_date - today).days` |

### Valid Categories List

```python
VALID_CATEGORIES = [
    'dairy', 'bakery', 'beverages', 'snacks',
    'frozen', 'meat', 'produce'
]
```

### Days Until Expiry — Date Handling

Oracle returns `DATE` fields as Python `datetime` objects. Extract `.date()` safely before calculating:

```python
def get_days_until_expiry(product):
    today  = date.today()
    expiry = product.get_expiry_date().date() \
             if hasattr(product.get_expiry_date(), 'date') \
             else product.get_expiry_date()
    return (expiry - today).days
```

---

## Main Flow — `main.py`

```
Step 1 — TAKE INPUTS AND VALIDATE
    ├── Input   : category, threshold
    ├── Validate: is_valid_category()
    └── Validate: is_valid_threshold()

Step 2 — FETCH AND DISPLAY PRODUCTS
    ├── Call    : retrieve_low_stock_products(category, threshold, conn)
    ├── If empty: print "No products found" and return
    ├── Print   : total products found
    └── For each product:
            ├── display_product()
            └── print days until expiry
```

---

## Sample Run

```
===================================
Enter the category   : Dairy
Enter the stock threshold : 20

Total products found : 2
-----------------------------------
Product ID   : P301
Product Name : Fresh Milk
Category     : Dairy
Price        : 45.0
Stock        : 10
Expiry Date  : 2024-08-15
-----------------------------------
Days Until Expiry : 36
-----------------------------------
Product ID   : P302
Product Name : Butter
Category     : Dairy
Price        : 120.0
Stock        : 5
Expiry Date  : 2024-08-20
-----------------------------------
Days Until Expiry : 41
-----------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid category input | `"Invalid Category"` |
| Threshold <= 0 | `"Invalid Threshold"` |
| No products match the filter | `"No products found"` |

---

## Key Python Concepts Used

```python
# Three WHERE conditions in one query
WHERE LOWER(category) = LOWER(:1)
  AND stock_quantity <= :2
  AND expiry_date > SYSDATE

# Two validations before querying
if not util.is_valid_category(category):
    print("Invalid Category")
    return
if not util.is_valid_threshold(threshold):
    print("Invalid Threshold")
    return

# Safe Oracle datetime to Python date conversion
expiry = product.get_expiry_date().date() \
         if hasattr(product.get_expiry_date(), 'date') \
         else product.get_expiry_date()

# Days remaining calculation
days_left = (expiry - date.today()).days
```
