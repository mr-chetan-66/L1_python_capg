# Problem 4 — Order Management System

## Overview

A Python + Oracle Database problem introducing the **INSERT** operation for the first time, combined with a SELECT to retrieve order history. Covers `conn.commit()`, error handling with `try/except`, and a **factory function** in util to build objects cleanly.

---

## File Structure

```
problem_4_order/
│
├── database.properties    → DB credentials config
├── order.py               → Entity class (6 fields, getters & setters)
├── order_dao.py           → DAO (2 DB functions — INSERT + SELECT)
├── order_util.py          → Utility helpers (validation, build, display, totals)
└── main.py                → Entry point (place order → view history)
```

---

## Oracle Table

```sql
CREATE TABLE orders (
    order_id      NUMBER PRIMARY KEY,
    customer_name VARCHAR2(100),
    product_id    NUMBER,
    quantity      NUMBER,
    order_date    DATE,
    status        VARCHAR2(20)
);
```

---

## Entity Class — `order.py`

| Field | Type | Description |
|-------|------|-------------|
| `order_id` | NUMBER | Primary key |
| `customer_name` | VARCHAR2(100) | Name of the customer |
| `product_id` | NUMBER | ID of the product ordered |
| `quantity` | NUMBER | Number of units ordered |
| `order_date` | DATE | Date the order was placed |
| `status` | VARCHAR2(20) | Order status (Pending / Shipped / Delivered / Cancelled) |

All fields are **private** with public getters and setters.

---

## DAO Functions — `order_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `place_order(order_obj, conn)` | INSERT | Inserts a new order into DB, commits, returns `True` on success or `False` on failure |
| `retrieve_orders_by_customer(customer_name, conn)` | SELECT | Fetch all orders for the given customer, ordered by `order_date DESC` |

### INSERT Logic

```python
def place_order(order_obj, conn):
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO orders (order_id, customer_name, product_id,
                                quantity, order_date, status)
            VALUES (:1, :2, :3, :4, :5, :6)
        """
        cursor.execute(insert_query, (
            order_obj.get_order_id(),
            order_obj.get_customer_name(),
            order_obj.get_product_id(),
            order_obj.get_quantity(),
            order_obj.get_order_date(),
            order_obj.get_status()
        ))
        conn.commit()
        cursor.close()
        return True
    except Exception:
        return False
```

### Key SQL — Fetch Order History

```sql
SELECT order_id, customer_name, product_id, quantity, order_date, status
FROM orders
WHERE LOWER(customer_name) = LOWER(:1)
ORDER BY order_date DESC
```

---

## Utility Functions — `order_util.py`

| Function | Description |
|----------|-------------|
| `build_order(order_id, customer_name, product_id, quantity)` | Creates and returns an `Order` object with `date.today()` and status `'Pending'` |
| `is_valid_quantity(quantity)` | Returns `True` only if quantity > 0 |
| `is_valid_status(status)` | Returns `True` if status is in valid statuses list |
| `display_order(order)` | Prints all order fields neatly |
| `get_result_count(list)` | Returns length of order list |
| `get_total_quantity_ordered(list)` | Returns sum of `quantity` across all orders |

### `build_order()` — Factory Helper

```python
def build_order(order_id, customer_name, product_id, quantity):
    return od.Order(
        order_id, customer_name, product_id,
        quantity, date.today(), 'Pending'   # auto-set date and status
    )
```

---

## Main Flow — `main.py`

```
Step 1 — PLACE A NEW ORDER
    ├── Input   : order_id, customer_name, product_id, quantity
    ├── Validate: is_valid_quantity()
    ├── Call    : util.build_order() to create Order object
    ├── Call    : dao.place_order(new_order, conn)
    └── Print   : "Order Placed Successfully" or "Order Placement Failed"

Step 2 — VIEW ORDER HISTORY
    ├── Call    : dao.retrieve_orders_by_customer(customer_name, conn)
    ├── Display : total orders and total items ordered
    └── Display : each order one by one
```

---

## Sample Run

```
===================================
       PLACE A NEW ORDER
===================================
Enter Order ID       : 5001
Enter Customer Name  : Priya Nair
Enter Product ID     : 201
Enter Quantity       : 3

Order Placed Successfully!

===================================
  ORDER HISTORY — PRIYA NAIR
===================================
Total Orders        : 2
Total Items Ordered : 7
-----------------------------------
Order ID      : 5001
Customer Name : Priya Nair
Product ID    : 201
Quantity      : 3
Order Date    : 2024-07-10
Status        : Pending
-----------------------------------
Order ID      : 4890
Customer Name : Priya Nair
Product ID    : 105
Quantity      : 4
Order Date    : 2024-06-22
Status        : Delivered
-----------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Quantity <= 0 | `"Invalid Quantity"` |
| DB insertion fails (duplicate ID etc.) | Returns `False` → prints `"Order Placement Failed"` |
| No orders found for customer | `"No orders found"` |

---

## Key Python Concepts Used

```python
# INSERT using getter methods of the object
cursor.execute(insert_query, (
    order_obj.get_order_id(),
    order_obj.get_customer_name(),
    ...
))

# Always commit after INSERT
conn.commit()

# Wrap INSERT in try/except to catch DB errors
try:
    ...
    return True
except Exception:
    return False

# Factory function — auto-sets date and status
od.Order(order_id, customer_name, product_id, quantity, date.today(), 'Pending')

# Sum of quantities using generator expression
sum(o.get_quantity() for o in order_list)
```
