### stock.py
### Entity class for Stock

class Stock:
    def __init__(self, stock_id, symbol, company_name,
                 sector, current_price, listed_date):
        self.__stock_id      = stock_id
        self.__symbol        = symbol           # e.g. 'INFY', 'TCS'
        self.__company_name  = company_name
        self.__sector        = sector           # e.g. 'IT', 'Banking', 'Pharma'
        self.__current_price = current_price    # float
        self.__listed_date   = listed_date      # datetime.date object

    def get_stock_id(self):
        return self.__stock_id

    def set_stock_id(self, v):
        self.__stock_id = v

    def get_symbol(self):
        return self.__symbol

    def set_symbol(self, v):
        self.__symbol = v

    def get_company_name(self):
        return self.__company_name

    def set_company_name(self, v):
        self.__company_name = v

    def get_sector(self):
        return self.__sector

    def set_sector(self, v):
        self.__sector = v

    def get_current_price(self):
        return self.__current_price

    def set_current_price(self, v):
        self.__current_price = v

    def get_listed_date(self):
        return self.__listed_date

    def set_listed_date(self, v):
        self.__listed_date = v
