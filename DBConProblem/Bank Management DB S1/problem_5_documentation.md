# Problem 5 — Bank Account Transaction System

## Overview

A Python + Oracle Database problem focused on **conditional UPDATE** with business logic — deposit adds to balance, withdrawal only succeeds if sufficient funds exist. Introduces the pattern of **fetch → validate → update → re-fetch** to show before and after state.

---

## File Structure

```
problem_5_bank/
│
├── database.properties    → DB credentials config
├── bank_account.py        → Entity class (6 fields, getters & setters)
├── bank_dao.py            → DAO (2 DB functions)
├── bank_util.py           → Utility helpers (validation, display, summary)
└── main.py                → Entry point (single transaction flow)
```

---

## Oracle Table

```sql
CREATE TABLE bank_account (
    account_number VARCHAR2(20) PRIMARY KEY,
    holder_name    VARCHAR2(100),
    account_type   VARCHAR2(30),
    balance        NUMBER(12,2),
    branch         VARCHAR2(100),
    ifsc_code      VARCHAR2(20)
);
```

---

## Entity Class — `bank_account.py`

| Field | Type | Description |
|-------|------|-------------|
| `account_number` | VARCHAR2(20) | Primary key |
| `holder_name` | VARCHAR2(100) | Account holder's name |
| `account_type` | VARCHAR2(30) | savings / current / salary / fixed deposit |
| `balance` | NUMBER(12,2) | Current account balance |
| `branch` | VARCHAR2(100) | Branch name |
| `ifsc_code` | VARCHAR2(20) | Bank IFSC code |

All fields are **private** with public getters and setters.

---

## DAO Functions — `bank_dao.py`

| Function | Operation | Description |
|----------|-----------|-------------|
| `retrieve_account(account_number, conn)` | SELECT | Fetch single account by account number, returns `None` if not found |
| `update_balance(account_number, amount, transaction_type, conn)` | SELECT + UPDATE | Validates account and balance, then updates and commits |

### Transaction Logic

```python
def update_balance(account_number, amount, transaction_type, conn):
    account = retrieve_account(account_number, conn)  # Step 1: check exists

    if account is None:
        return "Invalid Account"

    current_balance = account.get_balance()

    if transaction_type == 'deposit':
        new_balance = current_balance + amount          # Step 2a: deposit

    elif transaction_type == 'withdraw':
        if current_balance - amount < 0:
            return "Insufficient Balance"               # Step 2b: guard check
        new_balance = current_balance - amount

    # Step 3: UPDATE and commit
    return "Transaction Successful"
```

### Key SQL — Balance Update

```sql
UPDATE bank_account
SET balance = :1
WHERE account_number = :2
```

---

## Utility Functions — `bank_util.py`

| Function | Description |
|----------|-------------|
| `is_valid_transaction_type(type)` | Returns `True` if type is `'deposit'` or `'withdraw'` |
| `is_valid_amount(amount)` | Returns `True` only if amount > 0 |
| `display_account(account)` | Prints all account fields neatly |
| `display_transaction_summary(account_number, amount, type, updated_balance)` | Prints a clean summary of the transaction |

---

## Main Flow — `main.py`

```
Step 1 — TAKE INPUTS AND VALIDATE
    ├── Input   : account_number, amount, transaction_type
    ├── Validate: is_valid_transaction_type()
    └── Validate: is_valid_amount()

Step 2 — SHOW ACCOUNT BEFORE TRANSACTION
    ├── Call    : retrieve_account(account_number, conn)
    ├── If None : print "Invalid Account" and return
    └── Display : account details before transaction

Step 3 — PERFORM TRANSACTION
    ├── Call    : update_balance(account_number, amount, transaction_type, conn)
    ├── If "Insufficient Balance" : print and return
    └── If "Transaction Successful":
            ├── Re-fetch account to get updated balance
            └── Display : transaction summary with new balance
```

---

## Sample Run

```
======================================
       BANK ACCOUNT TRANSACTION
======================================
Enter Account Number           : ACC10234
Enter Amount                   : 5000
Enter Transaction Type         : withdraw

Account Details Before Transaction:
Account Number : ACC10234
Holder Name    : Ramesh Iyer
Account Type   : Savings
Balance        : 17500.0
Branch         : Chennai Main
IFSC Code      : SBIN0001234
--------------------------------------

Transaction Summary
--------------------------------------
Account Number   : ACC10234
Transaction Type : Withdraw
Amount           : 5000.0
Updated Balance  : 12500.0
--------------------------------------
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid transaction type | `"Invalid Transaction Type"` |
| Amount <= 0 | `"Invalid Amount"` |
| Account number not in DB | `"Invalid Account"` |
| Withdraw amount exceeds balance | `"Insufficient Balance"` |

---

## Key Python Concepts Used

```python
# Fetch before update to get current balance
account = retrieve_account(account_number, conn)
current_balance = account.get_balance()

# Deposit — simple addition
new_balance = current_balance + amount

# Withdrawal — guard check before subtraction
if current_balance - amount < 0:
    return "Insufficient Balance"
new_balance = current_balance - amount

# Re-fetch after update to confirm new balance
updated_account = retrieve_account(account_number, conn)
print("Updated Balance:", updated_account.get_balance())
```
