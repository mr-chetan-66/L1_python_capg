### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import flight as fl
import cx_Oracle
 
db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
   
#Creating Connection String
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
 
 
 
#### WRITE YOUR CODE HERE FOR THE FUNCTION
def retrieve_flight_by_id(flight_id,conn):
    cursor = conn.cursor()
    select = """SELECT * FROM flight WHERE flightId = :param1"""
    cursor.execute(select,param1=flight_id)
    row = cursor.fetchone()
    if row is not None:
        flight_obj = fl.Flight(row[0],row[1],row[2],row[3],row[4])
        return flight_obj
    else:
        return row
 
 
 
 
 #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
flight_id = int(input("Enter the flight id:"))
 
flight_obj = retrieve_flight_by_id(flight_id,conn)
 
if flight_obj == None:
    print("Invalid Flight ID")
else:
    print("Flight ID:", flight_obj.get_flight_id())
    print("Source:", flight_obj.get_source())
    print("Destination:", flight_obj.get_destination())
    print("No of seats:", flight_obj.get_no_of_seats())
    print("Flight Fare:", flight_obj.get_flight_fare())