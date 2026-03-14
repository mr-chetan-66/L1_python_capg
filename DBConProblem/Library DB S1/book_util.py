### book_util.py
### Utility / helper functions for Book — validation and display

VALID_GENRES = [
    'fiction', 'non-fiction', 'science', 'history',
    'biography', 'technology', 'mystery', 'fantasy',
    'romance', 'self-help'
]

VALID_ACTIONS = ['issue', 'return']


def is_valid_genre(genre):
    # Returns True if genre (case-insensitive) is in VALID_GENRES
    return genre.lower() in VALID_GENRES


def is_valid_action(action):
    # Returns True if action is 'issue' or 'return' (case-insensitive)
    return action.lower() in VALID_ACTIONS


def display_book(book):
    print("Book ID          :", book.get_book_id())
    print("Title            :", book.get_title())
    print("Author           :", book.get_author())
    print("Genre            :", book.get_genre())
    print("Available Copies :", book.get_available_copies())
    print("Issued Copies    :", book.get_issued_copies())
    print("-" * 40)


def get_result_count(book_list):
    return len(book_list)


def get_availability_status(book):
    # Returns 'Available' if available_copies > 0, else 'Not Available'
    if book.get_available_copies() > 0:
        return "Available"
    return "Not Available"


def get_total_copies(book):
    # Returns total copies = available_copies + issued_copies
    return book.get_available_copies() + book.get_issued_copies()
