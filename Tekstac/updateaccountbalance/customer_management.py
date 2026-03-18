### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import customer as ct
import cx_Oracle


db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])   

def update_account_balance(acc_type, conn):
    with conn.cursor() as cur:
        q="""select * from Bank 
        where acc_type=:1"""
        cur.execute(q,(acc_type,))
        ans=[]
        row =cur.fetchall()
        for r in row:
            obj=ct.Customer(*r)
            bal=obj.get_acc_balance()
            if acc_type == 'Savings' and bal>15000:
                bal=bal*1.07
            elif acc_type == 'Savings' and bal<=15000:
                bal=bal*1.05
            elif acc_type=='Current' and bal>15000:
                bal=bal*1.06
            elif acc_type == 'Current' and bal<=15000:
                bal=bal*1.04
                
            obj.set_acc_balance(bal)
            ans.append(obj)
        return ans
                
# #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
acc_type = input("Enter the Account type :")

li=update_account_balance(acc_type,conn)

print("Account number, Customer Name, Account Type, Available Balance")
for l in li:
    print(f"{l.get_acc_no()} {l.get_cust_name()} {acc_type} {l.get_acc_balance():.1f}")
        



