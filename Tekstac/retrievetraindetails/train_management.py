### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import train as tn
import cx_Oracle

class TrainManagementSystem:
    
    def __init__(self):
        self.db=""
        with open("database.properties") as f:
            self.lines=[line.strip().split("=") for line in f.readlines() if not line.startswith("#") and line.strip()]
            self.db={k.strip():v.strip() for k,v in self.lines}
            
        
    def retrieve_train_details(self, coach_type, source, destination):
        ans=[]
        
        try:
            self.conn=cx_Oracle.connect(self.db["DB_USERNAME"],self.db["DB_PASSWORD"],self.db["DSN"])
            
            with self.conn.cursor() as cur:
                
                q=f"""select train_number, train_name, source, destination,
                ac1, ac2, ac3, sleeper, seater from train 
                where {coach_type}>0
                and source=:s
                and destination=:d
                order by train_number"""
            
                cur.execute(q,(source,destination))
            
                row=cur.fetchall()
                
                for r in row:
                    obj=tn.train(*r)
                    ans.append(obj)
            
        except cx_Oracle.DatabaseError:
            return []
        
        return ans
    
    def view_train_details(self, l):
        for t in l:
            print(f"{t.get_train_number()} {t.get_train_name()}")
            