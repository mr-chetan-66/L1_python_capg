import sqlite3

conn = sqlite3.connect("database_table.db")  # or :memory:
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS service (
    service_id TEXT PRIMARY KEY,
    customer_name TEXT,
    service_date TEXT,
    service_type TEXT,
    base_charge REAL,
    service_charge REAL);
    """

cursor.execute(query)
conn.commit()
conn.close()

print("Database Created")