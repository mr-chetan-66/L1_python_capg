### book.py
### Entity class for Book

class Book:
    def __init__(self, book_id, title, author, genre, available_copies, issued_copies):
        self.__book_id           = book_id
        self.__title             = title
        self.__author            = author
        self.__genre             = genre
        self.__available_copies  = available_copies
        self.__issued_copies     = issued_copies

    def get_book_id(self):
        return self.__book_id

    def set_book_id(self, book_id):
        self.__book_id = book_id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_author(self):
        return self.__author

    def set_author(self, author):
        self.__author = author

    def get_genre(self):
        return self.__genre

    def set_genre(self, genre):
        self.__genre = genre

    def get_available_copies(self):
        return self.__available_copies

    def set_available_copies(self, available_copies):
        self.__available_copies = available_copies

    def get_issued_copies(self):
        return self.__issued_copies

    def set_issued_copies(self, issued_copies):
        self.__issued_copies = issued_copies
