import oracledb
import customer_db_setup as dbs
import customer_entity as ce

class CustomerRepository:

    def search_customer_by_id(self, customer_id,conn):
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM customer WHERE customer_id=:param""",{"param":customer_id})
            row=cur.fetchone()
            
            if row is None:
                return None
            
            cust_id, name, email, phone = row
            return ce.Customer(cust_id, name, email, phone)


# --- Optional quick demo ---
if __name__ == "__main__":
    # Ensure you ran customer_db_setup.py once before this.
    repo = CustomerRepository()
    dbs.start()
    
    db = ""

    # Load your properties file
    with open("database.properties") as f:
        lines = [
            line.strip().split("=")
            for line in f.readlines()
            if not line.startswith("#") and line.strip()
        ]
        db = {k.strip(): v.strip() for k, v in lines}

    # Connect to Oracle
    with oracledb.connect(
        user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"]
    ) as conn:
        found = repo.search_customer_by_id(101,conn)
        print("Search(101):", found)
        
        if found is None:
            print("Not Found (101)")
        else:
            print(found)


        not_found = repo.search_customer_by_id(9999,conn)
        print("Search(9999):", not_found)
        
        if not_found is None:
            print("Not Found")
        else:
            print(not_found)
    