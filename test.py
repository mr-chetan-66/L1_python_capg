# with open("data.txt","r") as f:
#     count=0
#     for line in f:
#         c=len(line.strip().split())
#         count+=c
        
#     print(count)
    

# import exception
import sqlite3

conn=sqlite3.connect("data.db")
cur=conn.cursor()

cur.execute("create table if not exists raw (name text,age integer)")
conn.commit()

cur=conn.cursor() 
l=[
    ("chetan",22),
    ("Anshul",22)
]
cur.executemany("insert into raw values (?,?)",l)
conn.commit()

cur.execute("select * from raw")
rows=cur.fetchall()

for row in rows:
    print(row)

cur.execute("delete from raw where name=?",("chetan",))
conn.commit()
cur.execute("select * from raw")
rows=cur.fetchall()

for row in rows:
    print(row)

conn.close()
        