import sqlite3

conn = sqlite3.connect("database_table.db")  # or :memory:
cursor = conn.cursor()

query = "DELETE FROM service"

cursor.execute(query)
conn.commit()
conn.close()

print("Data deleted")