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
        user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"]
    ) as conn:

        with conn.cursor() as cur:

            # Check if CUSTOMER table exists
            cur.execute(
                """
                SELECT COUNT(*)
                FROM user_tables
                WHERE table_name = :tbl
            """,
                {"tbl": "ATTENDANCE"},
            )  # Must always be uppercase

            (exists,) = cur.fetchone()

            if not exists:
                cur.execute(
                    """
                    CREATE TABLE attendance (
                    employee_id INTEGER NOT NULL,
                    att_date    DATE NOT NULL,
                    status      VARCHAR2(20),
                    CONSTRAINT att_pk PRIMARY KEY (employee_id, att_date)
                    )
                """)
                print("Table ATTENDANCE created.")
            else:
                print("Table ATTENDANCE already exists; skipping create.")

            # Insert sample rows (Oracle does NOT support multi-row INSERT syntax)
            rows = [
                (1, "2024-07-01", "Present"),
                (1, "2024-07-02", "Absent"),
                (2, "2024-07-01", "Present"),
                (3, "2024-07-01", "Present"),
                (3, "2024-07-02", "Present"),
            ]

            cur.executemany(
                "INSERT INTO attendance (employee_id, att_date, status) VALUES (:1, TO_DATE(:2,'YYYY-MM-DD'), :3)",
                rows,
            )

            conn.commit()
            print("Database initialized: Oracle with 'attendance' table and seed data.")
