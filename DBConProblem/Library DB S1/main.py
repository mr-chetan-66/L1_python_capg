### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import book_dao as dao
import book_util as util


def main():
    conn = db.get_connection()

    print("=" * 40)
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)

    # Step 1 — Search books by genre
    genre = input("Enter Genre to Search : ")

    if not util.is_valid_genre(genre):
        print("Invalid Genre")
        return

    books = dao.retrieve_books_by_genre(genre, conn)

    if not books:
        print("No books found in this genre")
        return

    print("\nTotal Books Found :", util.get_result_count(books))
    print("-" * 40)

    for book in books:
        util.display_book(book)
        print("Availability      :", util.get_availability_status(book))
        print("Total Copies      :", util.get_total_copies(book))
        print("-" * 40)

    # Step 2 — Perform issue or return action
    print("\n" + "=" * 40)
    book_id = int(input("Enter Book ID for Action  : "))
    action  = input("Enter Action (issue/return): ")

    if not util.is_valid_action(action):
        print("Invalid Action")
        return

    # Confirm book exists before action
    book = dao.retrieve_book_by_id(book_id, conn)
    if book is None:
        print("Invalid Book ID")
        return

    print("\nBook Details Before Action:")
    util.display_book(book)

    # Perform action
    if action.lower() == 'issue':
        result = dao.issue_book(book_id, conn)
    else:
        result = dao.return_book(book_id, conn)

    print("Status :", result)

    # Show updated book state
    if result in ("Book Issued Successfully", "Book Returned Successfully"):
        updated_book = dao.retrieve_book_by_id(book_id, conn)
        print("\nBook Details After Action:")
        util.display_book(updated_book)


if __name__ == '__main__':
    main()
