### product.py
### Entity class for Product

class Product:
    def __init__(self, product_id, product_name, category, price, stock_quantity, expiry_date):
        self.__product_id = product_id
        self.__product_name = product_name
        self.__category = category
        self.__price = price
        self.__stock_quantity = stock_quantity
        self.__expiry_date = expiry_date

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_product_name(self):
        return self.__product_name

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_stock_quantity(self):
        return self.__stock_quantity

    def set_stock_quantity(self, stock_quantity):
        self.__stock_quantity = stock_quantity

    def get_expiry_date(self):
        return self.__expiry_date

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date
