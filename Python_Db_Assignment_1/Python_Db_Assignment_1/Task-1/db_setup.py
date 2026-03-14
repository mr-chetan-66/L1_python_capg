import oracledb  # CHANGED from cx_Oracle to oracledb

def start():
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
        user=db["DB_USERNAME"],
        password=db["DB_PASSWORD"],
        dsn=db["DSN"]
    ) as conn:

        with conn.cursor() as cur:

            # Check if CUSTOMER table exists
            cur.execute("""
                SELECT COUNT(*)
                FROM user_tables
                WHERE table_name = :tbl
            """, {"tbl": "CUSTOMER"})  # Must always be uppercase

            (exists,) = cur.fetchone()

            if not exists:
                cur.execute("""
                    CREATE TABLE customer (
                        customer_id INTEGER PRIMARY KEY,
                        name        VARCHAR2(100) NOT NULL,
                        email       VARCHAR2(300) UNIQUE NOT NULL,
                        phone       VARCHAR2(20)
                    )
                """)
                print("Table CUSTOMER created.")
            else:
                print("Table CUSTOMER already exists; skipping create.")

            # Insert sample rows (Oracle does NOT support multi-row INSERT syntax)
            rows = [
                (101, 'Ananya Rao', 'ananya.rao@example.com', '+91-9876543210'),
                (102, 'Rahul Mehta', 'rahul.mehta@example.com', '+91-9811122233'),
                (103, 'Priya Singh', 'priya.singh@example.com', '+91-9900011122'),
                (104, 'Arjun Nair', 'arjun.nair@example.com', '+91-9845012345'),
                (105, 'Meera Iyer', 'meera.iyer@example.com', '+91-9988776655')
            ]

            cur.executemany(
                "INSERT INTO customer (customer_id, name, email, phone) VALUES (:1, :2, :3, :4)",
                rows
            )

            conn.commit()
            print("Database initialized: Oracle with 'customer' table and seed data.")
        