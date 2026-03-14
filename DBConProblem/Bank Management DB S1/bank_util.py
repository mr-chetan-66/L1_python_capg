### bank_util.py
### Utility / helper functions for BankAccount — validation and display

VALID_TRANSACTION_TYPES = ['deposit', 'withdraw']


def is_valid_transaction_type(transaction_type):
    return transaction_type.lower() in VALID_TRANSACTION_TYPES


def is_valid_amount(amount):
    return amount > 0


def display_account(account):
    print("Account Number :", account.get_account_number())
    print("Holder Name    :", account.get_holder_name())
    print("Account Type   :", account.get_account_type())
    print("Balance        :", account.get_balance())
    print("Branch         :", account.get_branch())
    print("IFSC Code      :", account.get_ifsc_code())
    print("-" * 38)


def display_transaction_summary(account_number, amount, transaction_type, updated_balance):
    print("-" * 38)
    print("Transaction Summary")
    print("-" * 38)
    print("Account Number   :", account_number)
    print("Transaction Type :", transaction_type.capitalize())
    print("Amount           :", amount)
    print("Updated Balance  :", updated_balance)
    print("-" * 38)
