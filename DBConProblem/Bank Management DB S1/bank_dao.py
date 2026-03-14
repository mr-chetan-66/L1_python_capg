### bank_dao.py
### Data Access Object — contains all DB operations for BankAccount

import bank_account as ba


def retrieve_account(account_number, conn):
    cursor = conn.cursor()

    query = """
        SELECT account_number, holder_name, account_type, balance, branch, ifsc_code
        FROM bank_account
        WHERE account_number = :1
    """

    cursor.execute(query, (account_number,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return ba.BankAccount(row[0], row[1], row[2], row[3], row[4], row[5])


def update_balance(account_number, amount, transaction_type, conn):
    # Step 1: Check if account exists
    account = retrieve_account(account_number, conn)

    if account is None:
        return "Invalid Account"

    current_balance = account.get_balance()

    # Step 2: Apply business logic
    if transaction_type == 'deposit':
        new_balance = current_balance + amount

    elif transaction_type == 'withdraw':
        if current_balance - amount < 0:
            return "Insufficient Balance"
        new_balance = current_balance - amount

    # Step 3: Update balance in DB and commit
    cursor = conn.cursor()

    update_query = """
        UPDATE bank_account
        SET balance = :1
        WHERE account_number = :2
    """

    cursor.execute(update_query, (new_balance, account_number))
    conn.commit()
    cursor.close()

    return "Transaction Successful"
