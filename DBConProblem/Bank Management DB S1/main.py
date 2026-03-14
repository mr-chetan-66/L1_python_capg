### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import bank_dao as dao
import bank_util as util


def main():
    conn = db.get_connection()

    print("=" * 38)
    print("       BANK ACCOUNT TRANSACTION")
    print("=" * 38)

    account_number   = input("Enter Account Number           : ")
    amount           = float(input("Enter Amount                   : "))
    transaction_type = input("Enter Transaction Type         : ")

    # Validate transaction type
    if not util.is_valid_transaction_type(transaction_type):
        print("Invalid Transaction Type")
        return

    # Validate amount
    if not util.is_valid_amount(amount):
        print("Invalid Amount")
        return

    # Show account details before transaction
    account = dao.retrieve_account(account_number, conn)

    if account is None:
        print("Invalid Account")
        return

    print("\nAccount Details Before Transaction:")
    util.display_account(account)

    # Perform the transaction
    result = dao.update_balance(account_number, amount, transaction_type.lower(), conn)

    if result == "Insufficient Balance":
        print("Insufficient Balance")
        return

    # Fetch updated account to get new balance
    updated_account = dao.retrieve_account(account_number, conn)

    # Show transaction summary
    util.display_transaction_summary(
        account_number,
        amount,
        transaction_type,
        updated_account.get_balance()
    )


if __name__ == '__main__':
    main()
