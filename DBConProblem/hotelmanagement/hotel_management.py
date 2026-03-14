### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import hotel as hl
import cx_Oracle
from datetime import date
 
db=""
with open("database.properties","r") as f:
    lines=[line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db={key.strip():value.strip() for key,value in lines}

conn=cx_Oracle.connect(db["DB_USERNAME"],db["DB_PASSWORD"],db["DSN"])
 
def  retrieve_customer_details(address,conn):
    #WRITE YOUR CODE HERE FOR IMPLEMENTING THE FUNCTION
    cursor = conn.cursor()
   
    query = """
        SELECT room_no, cust_name, address, phone_number, from_date, to_date
        FROM hotel
        WHERE address = :param1
        AND (to_date - from_date)>3
    """
    cursor.execute(query,param1=address)
    records = cursor.fetchall()
   
    if len(records) == 0:
        return []
    hotel_list = []
   
    for row in records:
        hotel_obj = hl.Hotel(
                row[0], row[1], row[2],
                row[3], row[4], row[5]
            )
        hotel_list.append(hotel_obj)
 
 
    return hotel_list
 
 #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
address = input("Enter the Address: ")
 
result = retrieve_customer_details(address,conn)
if not result:
    print("Invalid Address")
else:
    count=1
    for hotel in result:
        print("Customer details", count)
        print("Room no:", hotel.get_room_no())
        print("Customer Name:", hotel.get_cust_name())
        print("Phone Number:", hotel.get_phone_number())
        no_of_days =  (hotel.get_to_date()-hotel.get_from_date()).days
        print("No of days:", no_of_days)
        count+=1