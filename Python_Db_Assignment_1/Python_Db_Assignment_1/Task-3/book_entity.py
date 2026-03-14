class Book:
    
    # Define the parameterized constructor here
    def __init__(self, book_id, title, author, price):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__price = float(price)

    # Setters (optional)
    def set_book_id(self, value): self.__book_id = value
    def set_title(self, value): self.__title = value
    def set_author(self, value): self.__author = value
    def set_price(self, value): self.__price = float(value)

    # Getters
    def get_book_id(self): return self.__book_id
    def get_title(self): return self.__title
    def get_author(self): return self.__author
    def get_price(self): return self.__price

    def __repr__(self):
        return (f"Book(book_id={self.__book_id}, title='{self.__title}', "
                f"author='{self.__author}', price={self.__price})")