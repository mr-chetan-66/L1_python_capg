### book_dao.py
### Data Access Object — contains all DB operations for Book
### Includes SELECT by ID, SELECT by genre, and conditional UPDATE for issuing a book

import book as bk


def retrieve_book_by_id(book_id, conn):
    cursor = conn.cursor()

    query = """
        SELECT book_id, title, author, genre, available_copies, issued_copies
        FROM book
        WHERE book_id = :1
    """

    cursor.execute(query, (book_id,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return bk.Book(row[0], row[1], row[2], row[3], row[4], row[5])


def retrieve_books_by_genre(genre, conn):
    cursor = conn.cursor()

    query = """
        SELECT book_id, title, author, genre, available_copies, issued_copies
        FROM book
        WHERE LOWER(genre) = LOWER(:1)
        ORDER BY title ASC
    """

    cursor.execute(query, (genre,))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    book_list = []
    for row in rows:
        book_obj = bk.Book(row[0], row[1], row[2], row[3], row[4], row[5])
        book_list.append(book_obj)

    return book_list


def issue_book(book_id, conn):
    # Step 1: Check if book exists
    book = retrieve_book_by_id(book_id, conn)

    if book is None:
        return "Invalid Book ID"

    # Step 2: Check if copies are available
    if book.get_available_copies() <= 0:
        return "No Copies Available"

    # Step 3: Decrement available_copies, increment issued_copies and commit
    cursor = conn.cursor()

    update_query = """
        UPDATE book
        SET available_copies = available_copies - 1,
            issued_copies    = issued_copies    + 1
        WHERE book_id = :1
    """

    cursor.execute(update_query, (book_id,))
    conn.commit()
    cursor.close()

    return "Book Issued Successfully"


def return_book(book_id, conn):
    # Step 1: Check if book exists
    book = retrieve_book_by_id(book_id, conn)

    if book is None:
        return "Invalid Book ID"

    # Step 2: Check if any copies are actually issued
    if book.get_issued_copies() <= 0:
        return "No Issued Copies To Return"

    # Step 3: Increment available_copies, decrement issued_copies and commit
    cursor = conn.cursor()

    update_query = """
        UPDATE book
        SET available_copies = available_copies + 1,
            issued_copies    = issued_copies    - 1
        WHERE book_id = :1
    """

    cursor.execute(update_query, (book_id,))
    conn.commit()
    cursor.close()

    return "Book Returned Successfully"
