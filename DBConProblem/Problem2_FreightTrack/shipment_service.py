# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import freight_exception as ex
import oracledb
import utility as ut
import shipment as s
from datetime import timedelta

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class ShipmentService:

    def __init__(self):
        self.__shipment_list=[]

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute('truncate table Shipment')
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_freight_id(part[1])
                ut.validate_shipment_id(part[0])
                dd=ut.convert_date(part[5])
                bd=ut.convert_date(part[8])
                obj=s.Shipment(part[0],part[1],part[2],float(part[3]),int(part[4]),dd,part[6],part[7],bd)
                obj.calculate_all_charge()
                self.__shipment_list.append(obj)
            except (ex.InvalidFreightIdException,ex.InvalidShipmentIdException) as  e:
                print(e.get_message())
        return self.__shipment_list

    def add_shipment_details(self, obj_list):
        with conn.cursor() as cur:
            for obj in obj_list:
                q='insert into Shipment values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)'
                l=[obj.get_shipment_id(),
                    obj.get_freight_id(),
                    obj.get_client_name(),
                    obj.get_weight_kg(),
                    obj.get_no_of_days(),
                    obj.get_dispatch_date(),
                    obj.get_service_type(),
                    obj.get_status(),
                    obj.get_booking_date(),
                    obj.get_base_charge(),
                    obj.get_surcharge(),
                    obj.get_total_charge()]
                
                cur.execute(q,l)
                conn.commit()
        return None

    def find_top3_freight(self):
        with conn.cursor() as cur:
            q='select freight_id from Shipment'
            cur.execute(q)
            rows=cur.fetchall()
            
            cnt={}
            for f in rows:
                f=f[0]
                if f in cnt:
                    cnt[f]+=1
                else:
                    cnt[f]=1
            
            scnt=dict(sorted(cnt.items(), key=lambda x:x[1],reverse=True))
            ans={}
            i=0
            prev=0
            for k,v in scnt.items():
                if prev!=v:
                    i+=1
                    prev=v
                if i>3:
                    break
                ans[k]=v
                
            return ans            
            
    def search_shipment(self, shipment_id):
        with conn.cursor() as cur:
            q='select * from Shipment where shipment_id=:1'
            cur.execute(q,(shipment_id,))
            row=cur.fetchone()
            
            if row is None:
                return None
            obj=s.Shipment(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            obj.calculate_all_charge()
            return obj

    def find_delivery_dates(self, start_date, end_date):
        with conn.cursor() as cur:
            q='select shipment_id,dispatch_date,no_of_days from Shipment where no_of_days>4 and dispatch_date between :1 and :2'
            cur.execute(q,(start_date,end_date))
            rows=cur.fetchall()
            return {id:(d+timedelta(days=nd))for id,d,nd in rows}
            
    def update_surcharge(self, service_type):
        with conn.cursor() as cur:
            q='update Shipment set surcharge=surcharge*1.12,total_charge=base_charge+surcharge*1.12 where ervice_type=:1'
            cur.execute(q,(service_type,))
            conn.commit()
            
            q2='select * from Shipment where service_type=:1'
            cur.execute(q2,(service_type,))
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            else:
                ans=[]
                for r in rows:
                    obj=s.Shipment(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
                    obj.calculate_all_charge()
                    ans.append(obj)
                return ans
