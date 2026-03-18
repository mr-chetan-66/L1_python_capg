### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE

import cx_Oracle
import flight as fl
db={}
with open("database.properties") as f:
    lines=[line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    
    db={k.strip():v.strip() for k,v in lines}

conn=cx_Oracle.connect(db["DB_USERNAME"],db["DB_PASSWORD"],db["DSN"])    

#### WRITE YOUR CODE HERE FOR THE FUNCTION
def retrieve_flight_by_id(flight_id,conn):
    with conn.cursor() as cur:
        q="""select * from flight where flightId=:1"""
        cur.execute(q,(flight_id,))
        row=cur.fetchone()
        
        if row is None:
            return None
        else:
            return fl.Flight(row[0],row[1],row[2],row[3],row[4])
 
 
 
 #### WRITE YOUR CODE HERE FOR GETTING USER INPUTS, FUNCTION CALL AND OUTPUT STATEMENTS
flight_id = int(input("Enter the flight id:"))

row=retrieve_flight_by_id(flight_id,conn)

if row is None:
    print("Invalid Flight ID")
else:
    #print("Flight details are:")
    print("Flight ID:",row.get_flight_id())
    print("Source:",row.get_source())
    print("Destination:",row.get_destination())
    print("No of seats:",row.get_no_of_seats())
    print("Flight Fare:",row.get_flight_fare())
