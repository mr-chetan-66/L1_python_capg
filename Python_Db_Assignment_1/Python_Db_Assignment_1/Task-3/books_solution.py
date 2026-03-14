import oracledb
import book_entity as be
import books_db_setup as dbs

class BookRepository:

    def bulk_insert_books(self, book_list,conn):
        # Write your code here
        with conn.cursor() as cur:
            query="""INSERT INTO books (book_id, title, author, price)
            VALUES (:1,:2,:3,:4)"""
            for obj in book_list:
                cur.execute(query,(obj.get_book_id(),obj.get_title(),obj.get_author(),obj.get_price()))
        conn.commit()

        s=set()
        for r in book_list:
            set.add(r.get_book_id())
            
        return len(s)

# --- Optional quick demo ---
if __name__ == "__main__":
    # Ensure you ran books_db_setup.py once before this.
    repo = BookRepository()
    dbs.start()
    
    books = [
        be.Book(4, "Refactoring", "Martin Fowler", 650.00),
        be.Book(5, "Working Effectively with Legacy Code", "Michael Feathers", 600.00),
        be.Book(2, "The Pragmatic Programmer (Dup)", "Hunt & Thomas", 500.00),  # duplicate id -> skipped in fallback
    ]
    
    db=""
    with open("database.properties") as f:
        lines=[line.strip().split("=") for line in f.readlines() if not line.startswith("#") and line.strip()]
        db={k.strip():v.strip() for k,v in lines}

    conn=oracledb.connect(user=db["DB_USERNAME"],password=db["DB_PASSWORD"],dsn=db["DSN"])
    count = repo.bulk_insert_books(books,conn)
    print(f"Inserted {count} book records.")