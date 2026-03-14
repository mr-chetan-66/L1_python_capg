### product.py
### Entity class for Product

class Product:
    def __init__(self, product_id, product_name, category, quantity_in_stock,
                 reorder_level, unit_price, last_restocked_date):
        self.__product_id          = product_id
        self.__product_name        = product_name
        self.__category            = category
        self.__quantity_in_stock   = quantity_in_stock    # int
        self.__reorder_level       = reorder_level        # int (restock if stock <= this)
        self.__unit_price          = unit_price           # float
        self.__last_restocked_date = last_restocked_date  # datetime.date object

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

    def get_quantity_in_stock(self):
        return self.__quantity_in_stock

    def set_quantity_in_stock(self, quantity_in_stock):
        self.__quantity_in_stock = quantity_in_stock

    def get_reorder_level(self):
        return self.__reorder_level

    def set_reorder_level(self, reorder_level):
        self.__reorder_level = reorder_level

    def get_unit_price(self):
        return self.__unit_price

    def set_unit_price(self, unit_price):
        self.__unit_price = unit_price

    def get_last_restocked_date(self):
        return self.__last_restocked_date

    def set_last_restocked_date(self, last_restocked_date):
        self.__last_restocked_date = last_restocked_date
