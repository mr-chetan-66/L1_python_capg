# Problem 5 — Event Booking Management System

## Overview

A **multi-table** Python + Oracle Database connectivity problem using a **class-based DAO pattern**.
This problem covers SELECT across two related tables, 4-step ordered validation with custom exceptions, INSERT + UPDATE committed in a single atomic transaction, nested dictionary seat summary, and formatted booking confirmation file writing.

---

## File Structure

```
problem_5_event/
│
├── database.properties      → DB credentials config
├── event.py                 → Entity class (8 fields, getters & setters)
├── booking.py               → Entity class (6 fields, getters & setters)
├── exceptions.py            → 4 custom exception classes
├── event_dao.py             → Class-based DAO (3 DB methods + private row mapper)
├── event_util.py            → Utility helpers (seat summary dict, display, file export)
└── main.py                  → Entry point (3-step user flow)
```

---

## File Descriptions

| File | Role |
|------|------|
| `database.properties` | DB credentials config |
| `event.py` | Entity class — 8 fields, getters & setters |
| `booking.py` | Entity class — 6 fields, getters & setters |
| `exceptions.py` | 4 custom exceptions isolated in one place |
| `event_dao.py` | Class-based DAO — 3 public methods: SELECT by ID, SELECT upcoming, INSERT + UPDATE booking. Private `__map_row_to_event()` shared by both SELECTs |
| `event_util.py` | Helpers — nested seat summary dict, console display, booking confirmation file export |
| `main.py` | Entry point — 3-step flow: display upcoming → book tickets → export confirmation |

---

## Database Operations Summary

| Operation | Method | Business Rule |
|-----------|--------|---------------|
| **SELECT** | `retrieve_event_by_id()` | Raises `EventNotFoundException` if not found |
| **SELECT** | `retrieve_upcoming_events()` | `event_date >= today`; sorted by date ASC then time ASC; raises `EventNotFoundException` if empty |
| **INSERT + UPDATE** | `book_tickets()` | 4-step ordered validation; both ops committed in one transaction; `conn.rollback()` on `cx_Oracle.DatabaseError` |

---

## New Concepts vs Problem 6 (Crime Management)

| Concept | Details |
|---------|---------|
| **Two entity INSERTs** | `book_tickets()` does INSERT into `booking` AND UPDATE on `event` in one commit — two tables touched in one transaction |
| **Private row mapper** | `__map_row_to_event()` is a private method in the DAO — shared by `retrieve_event_by_id` and `retrieve_upcoming_events` to avoid code duplication |
| **time object handling** | `event_time` stored as `VARCHAR2(5)` in DB — parsed with `datetime.strptime(str(row[4]), "%H:%M").time()`; guarded with `hasattr(row[4], 'hour')` |
| **Nested dictionary** | `get_seat_availability_summary()` returns `{event_id: {event_name, total_seats, booked_seats, available_seats, occupancy_pct}}` |
| **booking_id formula** | `event_id * 1000 + datetime.now().second` |
| **occupancy_pct** | `round((booked_seats / total_seats) * 100, 2)` — guarded against division by zero |

---

## Oracle Tables

```sql
CREATE TABLE event (
    event_id      NUMBER PRIMARY KEY,
    event_name    VARCHAR2(100),
    venue         VARCHAR2(100),
    event_date    DATE,
    event_time    VARCHAR2(5),
    total_seats   NUMBER,
    booked_seats  NUMBER,
    ticket_price  NUMBER(10, 2)
);

CREATE TABLE booking (
    booking_id    NUMBER PRIMARY KEY,
    event_id      NUMBER,
    customer_name VARCHAR2(100),
    num_tickets   NUMBER,
    booking_date  DATE,
    total_amount  NUMBER(10, 2)
);
```

---

## Entity Class — `event.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | NUMBER | Primary key |
| `event_name` | VARCHAR2(100) | Name of the event |
| `venue` | VARCHAR2(100) | Venue name |
| `event_date` | DATE | Date of the event |
| `event_time` | VARCHAR2(5) | Start time in `HH:MM` format |
| `total_seats` | NUMBER | Total seating capacity |
| `booked_seats` | NUMBER | Seats already booked |
| `ticket_price` | NUMBER(10,2) | Price per ticket |

---

## Entity Class — `booking.py`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `booking_id` | NUMBER | Primary key (`event_id * 1000 + now().second`) |
| `event_id` | NUMBER | FK → event table |
| `customer_name` | VARCHAR2(100) | Name of the customer |
| `num_tickets` | NUMBER | Number of tickets booked |
| `booking_date` | DATE | Date booking was made (`date.today()`) |
| `total_amount` | NUMBER(10,2) | `num_tickets × ticket_price` |

---

## Exceptions — `exceptions.py`

| Exception | When Raised |
|-----------|-------------|
| `EventNotFoundException` | Event ID not found in DB OR no upcoming events exist |
| `EventExpiredException` | Event date is in the past |
| `InvalidTicketCountException` | `num_tickets < 1` |
| `SeatNotAvailableException` | Available seats < `num_tickets` |

---

## DAO Class — `event_dao.py`

```python
class EventDao:
    def __init__(self, conn): ...
```

### Public Methods

#### `retrieve_event_by_id(event_id)`
- Fetches a single `Event` by primary key
- Uses `__map_row_to_event()` for safe date/time parsing
- Raises `EventNotFoundException` if not found

#### `retrieve_upcoming_events()`
- Fetches all events where `event_date >= date.today()`
- Sorted by `event_date ASC`, then `event_time ASC`
- Uses `__map_row_to_event()` for each row
- Raises `EventNotFoundException` if none found

#### `book_tickets(event_id, customer_name, num_tickets)`
- Validates in this **exact order**:
  1. Event exists → `EventNotFoundException`
  2. `event_date >= today` → `EventExpiredException`
  3. `num_tickets >= 1` → `InvalidTicketCountException`
  4. `available_seats >= num_tickets` → `SeatNotAvailableException`
- INSERTs into `booking` and UPDATEs `event.booked_seats` in one `conn.commit()`
- Calls `conn.rollback()` on `cx_Oracle.DatabaseError`
- Returns a `Booking` object

### Private Method

#### `__map_row_to_event(row)`
- Shared by both SELECT methods
- Safely converts Oracle DATE → `date` using `hasattr(..., 'date')`
- Safely parses `VARCHAR2` time string → `time` using `datetime.strptime`
- Returns an `Event` object

---

## Utility Functions — `event_util.py`

| Function | Description |
|----------|-------------|
| `get_seat_availability_summary(event_list)` | Returns nested dict `{event_id: {event_name, total_seats, booked_seats, available_seats, occupancy_pct}}` |
| `display_upcoming_events(summary)` | Prints seat summary for each event to console |
| `export_booking_confirmation(booking_obj, event_obj, filename)` | Writes formatted confirmation to file; raises `IOError` on failure |

---

## Main Program Flow — `main.py`

```
Step 1 — UPCOMING EVENTS
    ├── Call: event_dao.retrieve_upcoming_events()
    ├── Call: util.get_seat_availability_summary(upcoming)
    └── Display: util.display_upcoming_events(summary)

Step 2 — BOOK TICKETS
    ├── Input: event_id, customer_name, num_tickets
    ├── Call: event_dao.book_tickets(event_id, customer_name, num_tickets)
    ├── Call: event_dao.retrieve_event_by_id(event_id)   ← re-fetch for updated seats
    └── Display: Booking ID + Total Amount

Step 3 — EXPORT BOOKING CONFIRMATION
    ├── Input: filename
    ├── Call: util.export_booking_confirmation(booking_obj, event_obj, filename)
    └── Display: confirmation message
```

---

## Sample Run

```
============================================================
          EVENT BOOKING MANAGEMENT SYSTEM
============================================================

--- UPCOMING EVENTS ---
Upcoming Events
============================================================
Event ID       : 301
Event Name     : Rock Night Live
Total Seats    : 500
Booked Seats   : 480
Available Seats: 20
Occupancy      : 96.0%
------------------------------------------------------------
Event ID       : 302
Event Name     : Comedy Carnival
Total Seats    : 200
Booked Seats   : 50
Available Seats: 150
Occupancy      : 25.0%
------------------------------------------------------------

--- BOOK TICKETS ---
Enter Event ID to Book     : 302
Enter Your Name            : Kavya Nair
Enter Number of Tickets    : 3

Booking Successful!
Booking ID   : 302045
Total Amount : Rs. 2400.0

--- EXPORT BOOKING CONFIRMATION ---
Enter Filename to Save Confirmation : booking_302.txt
Confirmation saved to booking_302.txt
```

---

## Error / Edge Case Handling

| Scenario | Response |
|----------|----------|
| Event ID not in DB | `EventNotFoundException` — "Event not found for the given ID." |
| No upcoming events | `EventNotFoundException` — "No upcoming events available." |
| Event date is in the past | `EventExpiredException` — "Cannot book tickets for a past event." |
| `num_tickets < 1` | `InvalidTicketCountException` — "Number of tickets must be at least 1." |
| Not enough seats | `SeatNotAvailableException` — "Not enough seats available. Only X seat(s) left." |
| DB error during booking | `conn.rollback()` called; `cx_Oracle.DatabaseError` re-raised |
| Confirmation file write fails | `IOError` raised from `export_booking_confirmation` |
| Non-numeric event_id / num_tickets | `ValueError` caught in `main()` |

---

## Key Python Concepts Used

```python
# Private shared row mapper inside DAO class
def __map_row_to_event(self, row):
    e_date = row[3].date() if hasattr(row[3], 'date') else row[3]
    e_time = datetime.strptime(str(row[4]), "%H:%M").time() \
             if not hasattr(row[4], 'hour') else row[4]
    return ev.Event(...)

# Ordered 4-step validation in book_tickets
if event_obj.get_event_date() < date.today():
    raise EventExpiredException(...)
if num_tickets < 1:
    raise InvalidTicketCountException(...)
available = total_seats - booked_seats
if available < num_tickets:
    raise SeatNotAvailableException(f"... Only {available} seat(s) left.")

# Atomic INSERT + UPDATE in single transaction
cursor.execute(insert_query, (...))   # booking row
cursor.execute(update_query, (...))   # event booked_seats
conn.commit()

# booking_id formula
booking_id = event_id * 1000 + datetime.now().second

# Nested dictionary seat summary
summary[e.get_event_id()] = {
    'available_seats' : total - booked,
    'occupancy_pct'   : round((booked / total) * 100, 2)
}
```

---

## Complete Problem Series Summary

| # | Topic | Operations |
|---|-------|------------|
| 1 | Student Topper | SELECT + filter + ORDER BY |
| 2 | Employee Payroll | SELECT + salary dict + experience calc + file report |
| 3 | Product Low Stock | SELECT + multi-condition + SYSDATE |
| 4 | Order Placement | INSERT + SELECT |
| **5** | **Event Booking** | **Two-table DAO + 4-step validation + INSERT+UPDATE transaction + nested dict + confirmation file** |
| 6 | Crime Record Management | Two-table DAO + Custom Exceptions + Dict Grouping + File Report |
| 7 | Library Book Issue | SELECT + atomic dual-column UPDATE |
| 8 | Courier Tracking | Two-table DAO + State-Machine + Bulk CSV + File Report |
| 9 | Exam Result | Class-based DAO + DELETE + subquery |
| 10 | Vehicle Rental | Class-based DAO + Full CRUD |
