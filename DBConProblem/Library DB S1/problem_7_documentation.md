# Problem 7 — Library Management System

## Overview

A Python + Oracle Database problem focused on **atomic dual-column UPDATE** for issuing and returning books, along with **SELECT by genre** and **availability validation** before any update.

---

## File Structure

```
problem_7_library/
│
├── database.properties    → DB credentials config
├── book.py                → Entity class (6 fields, getters & setters)
├── book_dao.py            → DAO (4 DB functions)
├── book_util.py           → Utility helpers (validation, display, status checks)
└── main.py                → Entry point (2-step user flow)
```

---

## Oracle Table

```sql
CREATE TABLE book (
    book_id          NUMBER PRIMARY KEY,
    title            VARCHAR2(200),
    author           VARCHAR2(100),
    genre            VARCHAR2(50),
    available_copies NUMBER,
    issued_copies    NUMBER
);
```

---

## Entity Class — `book.py`

| Field | Type | Description |
|-------|------|-------------|
| `book_id` | NUMBER | Primary key |
| `title` | VARCHAR2(200) | Book title |
| `author` | VARCHAR2(100) | Author name |
| `genre` | VARCHAR2(50) | Book genre |
| `available_copies` | NUMBER | Copies currently available |
| `issued_copies` | NUMBER | Copies currently issued out |

All fields are **private** with public getters and setters.

---

## DAO Functions — `book_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_book_by_id(book_id, conn)` | SELECT | Fetch single book by ID, returns `None` if not found |
| `retrieve_books_by_genre(genre, conn)` | SELECT | Fetch all books of given genre, ordered by title ASC |
| `issue_book(book_id, conn)` | UPDATE | Checks existence + availability, then decrements available / increments issued |
| `return_book(book_id, conn)` | UPDATE | Checks existence + issued count, then increments available / decrements issued |

### Key SQL — Atomic Dual-Column UPDATE

```sql
-- Issue a book
UPDATE book
SET available_copies = available_copies - 1,
    issued_copies    = issued_copies    + 1
WHERE book_id = :1

-- Return a book
UPDATE book
SET available_copies = available_copies + 1,
    issued_copies    = issued_copies    - 1
WHERE book_id = :1
```

### Issue Book Logic

```python
def issue_book(book_id, conn):
    book = retrieve_book_by_id(book_id, conn)   # check exists
    if book is None:
        return "Invalid Book ID"
    if book.get_available_copies() <= 0:
        return "No Copies Available"
    # UPDATE and commit
    return "Book Issued Successfully"
```

### Return Book Logic

```python
def return_book(book_id, conn):
    book = retrieve_book_by_id(book_id, conn)   # check exists
    if book is None:
        return "Invalid Book ID"
    if book.get_issued_copies() <= 0:
        return "No Issued Copies To Return"
    # UPDATE and commit
    return "Book Returned Successfully"
```

---

## Utility Functions — `book_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_genre(genre)` | Returns `True` if genre is in the valid genres list |
| `is_valid_action(action)` | Returns `True` if action is `'issue'` or `'return'` |
| `display_book(book)` | Prints all book fields neatly |
| `get_result_count(list)` | Returns length of book list |
| `get_availability_status(book)` | Returns `"Available"` if `available_copies > 0`, else `"Not Available"` |
| `get_total_copies(book)` | Returns `available_copies + issued_copies` |

### Valid Genres List

```python
VALID_GENRES = [
    'fiction', 'non-fiction', 'science', 'history',
    'biography', 'technology', 'mystery', 'fantasy',
    'romance', 'self-help'
]
```

---

## Main Flow — `main.py`

```
Step 1 — SEARCH BOOKS BY GENRE
    ├── Input   : genre
    ├── Validate: is_valid_genre()
    ├── Call    : retrieve_books_by_genre(genre, conn)
    └── Display : each book with availability status and total copies

Step 2 — ISSUE OR RETURN A BOOK
    ├── Input   : book_id, action (issue / return)
    ├── Validate: is_valid_action()
    ├── Display : book details BEFORE action
    ├── Call    : issue_book() or return_book() based on action
    ├── Print   : result status
    └── Display : book details AFTER action (if successful)
```

---

## Sample Run

```
========================================
       LIBRARY MANAGEMENT SYSTEM
========================================
Enter Genre to Search : Fiction

Total Books Found : 2
----------------------------------------
Book ID          : 701
Title            : The Alchemist
Author           : Paulo Coelho
Genre            : Fiction
Available Copies : 3
Issued Copies    : 2
----------------------------------------
Availability      : Available
Total Copies      : 5
----------------------------------------
Book ID          : 702
Title            : To Kill a Mockingbird
Author           : Harper Lee
Available Copies : 0
Issued Copies    : 4
----------------------------------------
Availability      : Not Available
Total Copies      : 4
----------------------------------------

Enter Book ID for Action   : 701
Enter Action (issue/return): issue

Book Details Before Action:
Available Copies : 3  |  Issued Copies : 2
----------------------------------------
Status : Book Issued Successfully

Book Details After Action:
Available Copies : 2  |  Issued Copies : 3
----------------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid genre input | `"Invalid Genre"` |
| No books found in genre | `"No books found in this genre"` |
| Invalid action input | `"Invalid Action"` |
| Book ID not in DB | `"Invalid Book ID"` |
| `available_copies == 0` on issue | `"No Copies Available"` |
| `issued_copies == 0` on return | `"No Issued Copies To Return"` |

---

## Key Python Concepts Used

```python
# Both columns updated in one single SQL statement (atomic)
SET available_copies = available_copies - 1,
    issued_copies    = issued_copies    + 1

# Availability check before update
if book.get_available_copies() <= 0:
    return "No Copies Available"

# Total copies — Python-side calculation
def get_total_copies(book):
    return book.get_available_copies() + book.get_issued_copies()

# Before and after state — fetch twice
book = dao.retrieve_book_by_id(book_id, conn)   # before
util.display_book(book)
result = dao.issue_book(book_id, conn)
updated_book = dao.retrieve_book_by_id(book_id, conn)  # after
util.display_book(updated_book)
```
