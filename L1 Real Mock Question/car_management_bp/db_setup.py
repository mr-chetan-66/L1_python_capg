import cx_Oracle
def start():
    db={}
    with open("database.properties") as f:
        lines=[line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
        db={k.strip():v.strip() for k,v in lines}
        conn=cx_Oracle.connect(db["DB_USERNAME"],db["DB_PASSWORD"],db["DSN"])
        cursor = conn.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS Car (
            rental_id TEXT,
            car_number TEXT,
            customer_name TEXT,
            basic_cost REAL,
            no_of_days INT,
            rental_date TEXT,
            total_amount REAL);
            """

        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()