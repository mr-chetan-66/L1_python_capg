import sqlite3

def start():
    conn = sqlite3.connect("cardatabase.db")  # or :memory:
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
    conn.close()