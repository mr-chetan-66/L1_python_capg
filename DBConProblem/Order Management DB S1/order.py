### order.py
### Entity class for Order

class Order:
    def __init__(self, order_id, customer_name, product_id, quantity, order_date, status):
        self.__order_id = order_id
        self.__customer_name = customer_name
        self.__product_id = product_id
        self.__quantity = quantity
        self.__order_date = order_date
        self.__status = status

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_customer_name(self):
        return self.__customer_name

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_order_date(self):
        return self.__order_date

    def set_order_date(self, order_date):
        self.__order_date = order_date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
