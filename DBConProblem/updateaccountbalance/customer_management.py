### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import customer as ct
import cx_Oracle


db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])   


def update_account_balance(acc_type, conn):
    cursor = conn.cursor()
    customer_list = []
    select_query = """SELECT ACC_NO, CUST_NAME, ACC_TYPE, ACC_BALANCE FROM BANK WHERE ACC_TYPE = :acc"""
    cursor.execute(select_query, acc=acc_type)
    rows = cursor.fetchall()
    for row in rows:
        acc_no = row[0]
        cust_name = row[1]
        acc_type_db = row[2]
        balance = row[3]
        if acc_type_db == "Savings":
            if balance > 15000:
                balance = balance * 1.07
            elif balance < 15000:
                balance = balance * 1.05

        elif acc_type_db == "Current":
            if balance > 15000:
                balance = balance * 1.06
            elif balance < 15000:
                balance = balance * 1.04

        customer_obj = ct.Customer(acc_no, cust_name, acc_type_db, balance)
        customer_list.append(customer_obj)

    return customer_list

# #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
acc_type = input("Enter the Account type :")

customer_list = update_account_balance(acc_type, conn)

if len(customer_list) == 0:
    print("Invalid Account Type")
else:
    print("Account number, Customer Name, Account Type, Available Balance")
    for cust in customer_list:
        print(str(cust.get_acc_no()) + " " + cust.get_cust_name() + " " +cust.get_acc_type() + " " +format(cust.get_acc_balance(), ".1f"))
