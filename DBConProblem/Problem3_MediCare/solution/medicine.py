from datetime import date

class Medicine:
    def __init__(self, stock_id:str, med_code:str, med_name:str, category:str,
                 unit_price:float, quantity:int, manufacture_date:date, expiry_date:date):
        self.__stock_id = stock_id
        self.__med_code = med_code
        self.__med_name = med_name
        self.__category = category
        self.__unit_price = unit_price
        self.__quantity = quantity
        self.__manufacture_date = manufacture_date
        self.__expiry_date = expiry_date
        self.__margin_amount = 0.0
        self.__selling_price = 0.0
        self.__total_stock_value = 0.0

    def get_stock_id(self): return self.__stock_id
    def get_med_code(self): return self.__med_code
    def get_med_name(self): return self.__med_name
    def get_category(self): return self.__category
    def get_unit_price(self): return self.__unit_price
    def get_quantity(self): return self.__quantity
    def get_manufacture_date(self): return self.__manufacture_date
    def get_expiry_date(self): return self.__expiry_date
    def get_margin_amount(self): return self.__margin_amount
    def get_selling_price(self): return self.__selling_price
    def get_total_stock_value(self): return self.__total_stock_value

    def set_stock_id(self, v): self.__stock_id = v
    def set_med_code(self, v): self.__med_code = v
    def set_med_name(self, v): self.__med_name = v
    def set_category(self, v): self.__category = v
    def set_unit_price(self, v): self.__unit_price = v
    def set_quantity(self, v): self.__quantity = v
    def set_manufacture_date(self, v): self.__manufacture_date = v
    def set_expiry_date(self, v): self.__expiry_date = v
    def set_margin_amount(self, v): self.__margin_amount = v
    def set_selling_price(self, v): self.__selling_price = v
    def set_total_stock_value(self, v): self.__total_stock_value = v

    def calculate_selling_price(self):
        rates = {"Tablet": 0.12, "Capsule": 0.18, "Syrup": 0.10}
        rate = rates.get(self.__category, 0.08)
        margin = self.__unit_price * rate
        selling = self.__unit_price + margin
        total = selling * self.__quantity
        self.__margin_amount = margin
        self.__selling_price = selling
        self.__total_stock_value = total
        return margin
