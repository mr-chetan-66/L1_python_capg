# Please do not change the skelecton code given here
# You can add any number of methods and attributes as you required without changing the given template
import utility as ut
import car as cr
from datetime import datetime,timedelta
import oracledb
import invalid_exception as ex

db={}
with open("database.properties") as f:
    lines=[line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db={k.strip():v.strip() for k,v in lines}
    conn=oracledb.connect(user=db["DB_USERNAME"],password=db["DB_PASSWORD"],dsn=db["DSN"])
    
class CarService:
    
    def __init__(self):
        self.__discount_dict={}
    
    def read_data(self,file_obj):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE Car")
        for line in file_obj:
            part=line.strip().split(",")
            try:
                ut.validate_car_number(part[1])
                d=ut.convert_date(part[5])
                obj=cr.Car(part[0],part[1],part[2],float(part[3]),int(part[4]),d)
                dis=obj.calculate_total_amount()
                self.add_car_details(obj)
                if obj.get_no_of_days()>1:
                    self.__discount_dict[obj.get_rental_id()]=dis
            except ex.InvalidCarNumberException as e:
                print(e.get_message())
            
        return None
            
    def add_car_details(self,o):
        with conn.cursor() as cur:
            q='insert into Car values(:1,:2,:3,:4,:5,:6,:7)'
            l=[o.get_rental_id(),o.get_car_number(),o.get_customer_name(),o.get_basic_cost(),o.get_no_of_days(),o.get_rental_date(),o.get_total_amount()]
            cur.execute(q,l)
            conn.commit()
            return None
        
    def find_top3_rentals(self):
        with conn.cursor() as cur:
            q="select * from Car"
            
            cur.execute(q)
            
            rows=cur.fetchall()
            carDict = {}
            for row in rows:
                if row[1] in carDict:
                    carDict[row[1]]+=1
                else:
                    carDict[row[1]]=1
            
            sortedDict = dict(sorted(carDict.items(),key= lambda x:x[1],reverse=True))

            resDict = {}
            i = 0
            prev = 0
            for x,y in sortedDict.items():
                if y!=prev:
                    prev = y
                    i+=1
                #resDict[x] = y
                if i > 3:
                    break
                resDict[x] = y
                
            return resDict
        

    def find_closing_date(self,start_date,end_date):
        with conn.cursor() as cur:
            q="""select rental_id,rental_date,no_of_days from Car where no_of_days>3
            and rental_date between :1 and :2"""
            
            cur.execute(q,(start_date,end_date))
            
            row=cur.fetchall()
            
            return {id:(d+timedelta(days=nd)) for id,d,nd in row}

    
    
    
    
   
        
	
