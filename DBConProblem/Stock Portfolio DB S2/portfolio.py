### portfolio.py
### Entity class for Portfolio

class Portfolio:
    def __init__(self, portfolio_id, investor_name, stock_id,
                 symbol, quantity, buy_price, buy_date):
        self.__portfolio_id  = portfolio_id
        self.__investor_name = investor_name
        self.__stock_id      = stock_id
        self.__symbol        = symbol
        self.__quantity      = quantity    # int — number of shares held
        self.__buy_price     = buy_price   # float — price paid per share
        self.__buy_date      = buy_date    # datetime.date object

    def get_portfolio_id(self):
        return self.__portfolio_id

    def set_portfolio_id(self, v):
        self.__portfolio_id = v

    def get_investor_name(self):
        return self.__investor_name

    def set_investor_name(self, v):
        self.__investor_name = v

    def get_stock_id(self):
        return self.__stock_id

    def set_stock_id(self, v):
        self.__stock_id = v

    def get_symbol(self):
        return self.__symbol

    def set_symbol(self, v):
        self.__symbol = v

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, v):
        self.__quantity = v

    def get_buy_price(self):
        return self.__buy_price

    def set_buy_price(self, v):
        self.__buy_price = v

    def get_buy_date(self):
        return self.__buy_date

    def set_buy_date(self, v):
        self.__buy_date = v
