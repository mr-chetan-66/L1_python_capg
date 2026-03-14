import oracledb
import db_setup as dbs
import customer_entity as ce


class CustomerRepository:
    def add_customer_details(self, customer_list,conn):
        # Write your code here
        insert=0
        query="""
        INSERT INTO customer(customer_id, name, email, phone)
        VALUES (:1,:2,:3,:4)
        """
        
        for c in customer_list:
            with conn.cursor() as cur:
                try:
                    cur.execute(query,(c.get_customer_id(),c.get_name(),c.get_email(),c.get_phone()))
                    insert+=1
                except oracledb.DatabaseError as e:
                    err=e.args[0]
                    if err.code!=1:
                        raise
        
        conn.commit()         
        #return number of records added successfuly to db
        return insert


# --- Optional quick demo ---
if __name__ == "__main__":
    
    repo = CustomerRepository()
    dbs.start()
    
    # Prepare some new customers (one duplicate email to test IntegrityError handling)
    customers = [
        ce.Customer(201, "Neha Kulkarni", "neha.kulkarni@example.com", "+91-9012345678"),
        ce.Customer(202, "Aditya Verma", "aditya.verma@example.com", "+91-9023456789"),
        ce.Customer(203, "Pooja Bhat", "pooja.bhat@example.com", "+91-9034567890"),
        ce.Customer(204, "Harsh Vardhan", "harsh.vardhan@example.com", "+91-9045678901"),
        ce.Customer(205, "Shruti Gupta", "shruti.gupta@example.com", "+91-9056789012"),
        # Duplicate test (email already exists in seed -> should be skipped)
        ce.Customer(206, "Priya S", "priya.singh@example.com", "+91-9000000000"),
    ]
    
    db = ""
    with open("database.properties") as f:
        lines = [line.strip().split("=") for line in f.readlines() if not line.startswith("#") and line.strip()]
        db = {k.strip(): v.strip() for k, v in lines}

    conn = oracledb.connect(user=db["DB_USERNAME"],password=db["DB_PASSWORD"],dsn=db["DSN"])

    count = repo.add_customer_details(customers,conn)
    print(f"Inserted {count} new customers.")