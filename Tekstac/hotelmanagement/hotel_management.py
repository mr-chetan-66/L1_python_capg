### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import hotel as hl
import cx_Oracle
from datetime import date
 
db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
 
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
 
def  retrieve_customer_details(address,conn):
    #WRITE YOUR CODE HERE FOR IMPLEMENTING THE FUNCTION
    q="""select * from hotel
    where (to_date - from_date)>3
    and address=:1"""
    
    cur=conn.cursor()
    cur.execute(q,(address,))
    
    row=cur.fetchall()
    ans=[]
    for r in row:
        ans.append(hl.Hotel(*r))
        
    return ans
 
 #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
address = input("Enter the Address: ")

l=retrieve_customer_details(address,conn)

if not l:
    print("Invalid Address")
else:
    cnt=1
    for c in l:
        print(f"Customer details {cnt}")
        print(f"Room no:{c.get_room_no()}")
        print(f"Customer Name: {c.get_cust_name()}")
        print(f"Phone Number: {c.get_phone_number()}")
        nd=(c.get_to_date()-c.get_from_date()).days
        print(f"No of days: {nd}")
        cnt+=1