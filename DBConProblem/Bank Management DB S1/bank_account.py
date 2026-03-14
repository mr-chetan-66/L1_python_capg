### bank_account.py
### Entity class for BankAccount

class BankAccount:
    def __init__(self, account_number, holder_name, account_type, balance, branch, ifsc_code):
        self.__account_number = account_number
        self.__holder_name    = holder_name
        self.__account_type   = account_type
        self.__balance        = balance
        self.__branch         = branch
        self.__ifsc_code      = ifsc_code

    def get_account_number(self):
        return self.__account_number

    def set_account_number(self, account_number):
        self.__account_number = account_number

    def get_holder_name(self):
        return self.__holder_name

    def set_holder_name(self, holder_name):
        self.__holder_name = holder_name

    def get_account_type(self):
        return self.__account_type

    def set_account_type(self, account_type):
        self.__account_type = account_type

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

    def get_branch(self):
        return self.__branch

    def set_branch(self, branch):
        self.__branch = branch

    def get_ifsc_code(self):
        return self.__ifsc_code

    def set_ifsc_code(self, ifsc_code):
        self.__ifsc_code = ifsc_code
