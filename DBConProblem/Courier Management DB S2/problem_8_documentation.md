# Problem 8 — Courier Tracking System

## Overview

A **multi-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers SELECT across two related tables, state-machine transition validation via custom exceptions, date/time manipulation, tiered pricing calculation, bulk file reading, and formatted file writing.

---

## File Structure

```
problem_8_courier/
│
├── database.properties      → DB credentials config
├── bulk_updates.csv         → Sample bulk status update input file
├── shipment.py              → Entity class (10 fields, getters & setters)
├── tracking_event.py        → Entity class (5 fields, getters & setters)
├── exceptions.py            → 4 custom exception classes
├── shipment_dao.py          → Class-based DAO (3 DB methods + transition constants)
├── courier_util.py          → Utility helpers (metrics, display, file read/write)
└── main.py                  → Entry point (4-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `bulk_updates.csv` | Sample CSV for bulk status updates |
| `shipment.py` | Entity class — 10 fields, getters & setters |
| `tracking_event.py` | Entity class — 5 fields, getters & setters |
| `exceptions.py` | 4 custom exceptions isolated in one place |
| `shipment_dao.py` | Class-based DAO — 3 methods: SELECT by tracking number, SELECT tracking history, UPDATE status + INSERT event in one transaction. Also holds `VALID_TRANSITIONS` and `STATUS_PIPELINE` constants |
| `courier_util.py` | Helpers — metrics calculation, display, bulk CSV read, report file write |
| `main.py` | Entry point — 4-step flow: retrieve → update status → bulk update → export report |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_shipment_by_tracking()` | Raises `ShipmentNotFoundException` if not found |
| **SELECT** | `retrieve_tracking_history()` | Returns empty list (not exception) if no events |
| **UPDATE + INSERT** | `update_shipment_status()` | State-machine validated; both ops committed in one transaction with rollback on error |

---

## New Concepts vs Problem 10 (Vehicle Rental)

| Concept | Details |
|---------|---------|
| **Two-table system** | `shipment` + `tracking_event` — two entity classes, two SELECT queries |
| **Custom exceptions** | 4 exceptions in dedicated `exceptions.py` instead of string return values |
| **State-machine transitions** | `VALID_TRANSITIONS` dict enforces pipeline: Booked → In Transit → Out for Delivery → Delivered/Returned |
| **Atomic transaction** | UPDATE + INSERT committed together; `conn.rollback()` on `cx_Oracle.DatabaseError` |
| **Date/time split** | `dispatch_date` is `date`, `event_datetime` is `datetime` — handled separately |
| **Tiered pricing** | 3-tier shipping cost based on `weight_kg` |
| **Bulk file read** | CSV file processed line-by-line; errors caught per line without stopping |
| **Report file write** | Formatted `.txt` report written in overwrite mode |

---

## Oracle Tables

```sql
CREATE TABLE shipment (
    shipment_id             NUMBER PRIMARY KEY,
    tracking_number         VARCHAR2(20) UNIQUE,
    sender_name             VARCHAR2(100),
    receiver_name           VARCHAR2(100),
    origin_city             VARCHAR2(100),
    destination_city        VARCHAR2(100),
    dispatch_date           DATE,
    expected_delivery_date  DATE,
    weight_kg               NUMBER(8, 2),
    status                  VARCHAR2(30)
);

CREATE TABLE tracking_event (
    event_id          NUMBER PRIMARY KEY,
    shipment_id       NUMBER,
    event_datetime    TIMESTAMP,
    location          VARCHAR2(100),
    event_description VARCHAR2(300)
);
```

---

## Entity Class — `shipment.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `shipment_id` | NUMBER | Primary key |
| `tracking_number` | VARCHAR2(20) | Unique alphanumeric tracking number |
| `sender_name` | VARCHAR2(100) | Sender's full name |
| `receiver_name` | VARCHAR2(100) | Receiver's full name |
| `origin_city` | VARCHAR2(100) | City of origin |
| `destination_city` | VARCHAR2(100) | Destination city |
| `dispatch_date` | DATE | Date the shipment was dispatched |
| `expected_delivery_date` | DATE | Expected delivery date |
| `weight_kg` | NUMBER(8,2) | Weight in kilograms |
| `status` | VARCHAR2(30) | Current pipeline status |

All fields are **private** with public getters and setters following encapsulation principles.

---

## Entity Class — `tracking_event.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | NUMBER | Primary key |
| `shipment_id` | NUMBER | Foreign key → shipment |
| `event_datetime` | TIMESTAMP | Exact datetime of the event |
| `location` | VARCHAR2(100) | Location at time of event |
| `event_description` | VARCHAR2(300) | Description of what happened |

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `ShipmentNotFoundException` | Tracking number not found in DB |
| `DeliveredShipmentException` | Shipment is already `Delivered` or `Returned` |
| `InvalidStatusTransitionException` | `new_status` not in `VALID_TRANSITIONS[current_status]` |
| `TrackingFileReadException` | Bulk CSV file cannot be opened |

---

## DAO Class — `shipment_dao.py`

```python
class ShipmentDao:
    def __init__(self, conn): ...
```

### Constants (module-level)

```python
STATUS_PIPELINE = ['Booked', 'In Transit', 'Out for Delivery', 'Delivered', 'Returned']

VALID_TRANSITIONS = {
    'Booked'           : ['In Transit'],
    'In Transit'       : ['Out for Delivery', 'Returned'],
    'Out for Delivery' : ['Delivered', 'Returned'],
    'Delivered'        : [],
    'Returned'         : []
}
```

### Methods

#### `retrieve_shipment_by_tracking(tracking_number)`
- Fetches a single `Shipment` object by tracking number
- Safely converts Oracle datetime to `date` using `hasattr(..., 'date')`
- Raises `ShipmentNotFoundException` if not found

#### `retrieve_tracking_history(shipment_id)`
- Fetches all `TrackingEvent` objects for the given shipment
- Ordered by `event_datetime ASC`
- Returns empty list `[]` if no events exist — does NOT raise

#### `update_shipment_status(tracking_number, new_status, location, description)`
- Validates in order: exists → not terminal → valid transition
- UPDATEs `shipment.status` and INSERTs into `tracking_event` in one transaction
- `event_id` calculated as `shipment_id * 100 + datetime.now().second`
- Calls `conn.rollback()` on `cx_Oracle.DatabaseError`
- Returns `"Status updated to <new_status>."`

---

## Utility Functions — `courier_util.py`

| Function | Description |
|----------|-------------|
| `calculate_delivery_metrics(shipment_obj)` | Returns dict with `days_in_transit`, `days_until_due`, `is_overdue`, `shipping_cost` |
| `display_shipment(shipment_obj, metrics)` | Prints all shipment fields and metrics to console |
| `display_tracking_history(tracking_history)` | Prints each event chronologically; prints "No events recorded yet." if empty |
| `load_bulk_status_updates_from_file(filepath, shipment_dao)` | Reads CSV, calls `shipment_dao.update_shipment_status()` per line, returns list of result tuples |
| `export_shipment_report(shipment_obj, tracking_history, metrics, filename)` | Writes formatted `.txt` report in overwrite mode; raises `IOError` if write fails |

### Shipping Cost Tiers

| Weight | Rate per kg | Formula |
|--------|-------------|---------|
| `weight_kg <= 5` | Rs. 50.0 | `weight * 50.0` |
| `5 < weight_kg <= 20` | Rs. 40.0 | `weight * 40.0` |
| `weight_kg > 20` | Rs. 30.0 | `weight * 30.0` |

---

## Main Program Flow — `main.py`

```
Step 1 — RETRIEVE SHIPMENT
    ├── Input: tracking_number
    ├── Call: shipment_dao.retrieve_shipment_by_tracking(tracking_number)
    ├── Call: shipment_dao.retrieve_tracking_history(shipment_id)
    ├── Call: util.calculate_delivery_metrics(shipment_obj)
    └── Display: shipment details + metrics + tracking history

Step 2 — UPDATE SHIPMENT STATUS
    ├── Input: new_status, location, description
    ├── Call: shipment_dao.update_shipment_status(...)
    └── Display: result message

Step 3 — BULK STATUS UPDATE FROM FILE
    ├── Input: CSV filepath (optional — press Enter to skip)
    ├── Call: util.load_bulk_status_updates_from_file(filepath, shipment_dao)
    └── Display: result tuple for each line (SUCCESS / FAILED)

Step 4 — EXPORT SHIPMENT REPORT
    ├── Input: output filename
    ├── Refresh: retrieve_tracking_history() to include updates from Steps 2 & 3
    ├── Call: util.export_shipment_report(shipment_obj, history, metrics, filename)
    └── Display: confirmation message
```

---

## Sample Run

```
==================================================
         COURIER TRACKING SYSTEM
==================================================

--- RETRIEVE SHIPMENT ---
Enter Tracking Number : TRK-1001

Shipment Found : TRK-1001
Status         : In Transit
Route          : Mumbai -> Bangalore
Sender         : Arjun Mehta
Receiver       : Sneha Rao
Weight         : 3.5 kg
Days In Transit: 4
Days Until Due : 0
Overdue        : No
Shipping Cost  : Rs. 175.0
--------------------------------------------------

Tracking History:
  01-08-2024 09:00  [Mumbai Hub]  Shipment booked and dispatched
  02-08-2024 14:30  [Pune Transit]  Package in transit via Pune

--- UPDATE SHIPMENT STATUS ---
Enter New Status       : Out for Delivery
Enter Current Location : Bangalore Outpost
Enter Event Description: Package reached Bangalore outpost, out for delivery
Update Status : Status updated to Out for Delivery.

--- BULK STATUS UPDATE FROM FILE ---
Enter Bulk Update CSV File Path (or press Enter to skip) : bulk_updates.csv

Bulk Update Results:
--------------------------------------------------
  TRK-1002 -> [SUCCESS] Status updated to In Transit.
  TRK-1003 -> [SUCCESS] Status updated to Out for Delivery.
  TRK-1004 -> [SUCCESS] Status updated to Delivered.

--- EXPORT SHIPMENT REPORT ---
Enter Filename to Export Report : TRK1001_report.txt
Shipment report exported to TRK1001_report.txt
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Tracking number not in DB | `ShipmentNotFoundException` — "No shipment found for tracking number: TRK-9999" |
| Status is already Delivered or Returned | `DeliveredShipmentException` — "Shipment is already Delivered and cannot be updated." |
| Invalid status transition | `InvalidStatusTransitionException` — "Invalid transition: In Transit -> Delivered" |
| Bulk CSV file not found | `TrackingFileReadException` — "Could not read update file: bulk_updates.csv" |
| Malformed CSV line (< 4 fields) | Per-line FAILED result — "Malformed line — expected 4 fields." |
| DB error during UPDATE/INSERT | `conn.rollback()` called; `cx_Oracle.DatabaseError` re-raised |
| Report file write fails | `IOError` raised from `export_shipment_report` |
| No tracking events yet | Returns `[]` from DAO; prints "No events recorded yet." |

---

## Key Python Concepts Used

```python
# State-machine transition validation
if new_status not in VALID_TRANSITIONS.get(current_status, []):
    raise InvalidStatusTransitionException(
        f"Invalid transition: {current_status} -> {new_status}")

# Atomic UPDATE + INSERT with rollback
try:
    cursor.execute(update_query, (...))
    cursor.execute(insert_query, (...))
    conn.commit()
except cx_Oracle.DatabaseError:
    conn.rollback()
    raise

# Safely handle Oracle TIMESTAMP vs Python datetime
evt_dt = row[2] if isinstance(row[2], datetime) \
         else datetime.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S")

# Safely handle Oracle DATE vs Python date
dispatch_date = row[6].date() if hasattr(row[6], 'date') else row[6]

# Tiered shipping cost
weight = shipment_obj.get_weight_kg()
if weight <= 5:
    shipping_cost = round(weight * 50.0, 2)
elif weight <= 20:
    shipping_cost = round(weight * 40.0, 2)
else:
    shipping_cost = round(weight * 30.0, 2)

# Per-line exception handling in bulk update — does not stop on failure
try:
    msg = shipment_dao.update_shipment_status(...)
    results.append((tracking_number, 'SUCCESS', msg))
except Exception as e:
    results.append((tracking_number, 'FAILED', str(e)))

# event_id generation
event_id = shipment_id * 100 + datetime.now().second
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Salary Range | SELECT + BETWEEN |
| 3 | Product Low Stock | SELECT + multi-condition + SYSDATE |
| 4 | Order Placement | INSERT + SELECT |
| 5 | Bank Account Transaction | SELECT + conditional UPDATE |
| 6 | Doctor Search | SELECT + dual filter + lambda highlight |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| **8** | **Courier Tracking** | **Two-table DAO + Custom Exceptions + State-Machine + Bulk CSV + File Report** |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
