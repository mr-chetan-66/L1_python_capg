import oracledb

def start():
    db=""
    with open("database.properties") as f:
        lines=[line.strip().split("=") for line in f.readlines() if not line.startswith("#") and line.strip()]
        db={k.strip():v.strip() for k,v in lines}
    
    with oracledb.connect(user=db["DB_USERNAME"],password=db["DB_PASSWORD"],dsn=db["DSN"]) as conn:
        with conn.cursor() as cur:
            
            cur.execute("""
                        SELECT COUNT(*) FROM user_tables
                        WHERE table_name=:tbn""",{"tbn":"BOOKS"})
            
            (exist,)=cur.fetchone()
            
            if not exist:
                cur.execute("""
                    CREATE TABLE books(
                    book_id INTEGER PRIMARY KEY,
                    title VARCHAR2(255) NOT NULL,
                    author VARCHAR2(255) NOT NULL,
                    price NUMBER(10,2) NOT NULL
                    )
                """)
                print("Table BOOKS created.")
            else:
                print("Table BOOKS already exists; skipping create.")
                
            books=[
                (1, 'Clean Code', 'Robert C. Martin', 450.00),
                (2, 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 550.00),
                (3, 'Design Patterns', 'Erich Gamma et al.', 700.00)]
            
            query="""INSERT INTO books (book_id, title, author, price)
            VALUES (:1,:2,:3,:4)"""
            cur.executemany(query,books)
            
            conn.commit()
            print("Database initialized: Oracle with 'books' table and seed data.")

            