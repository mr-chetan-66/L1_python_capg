# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import med_exception as ex
import utility as ut
import medicine as m
from datetime import timedelta

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class MedService:

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute('truncate table Medicine')
        for line in records:
            part=line.strip().split(",")
            try: 
                ut.validate_stock_id(part[0])
                ut.validate_med_code(part[1])
    
                ed=ut.convert_date(part[7])
                md=ut.convert_date(part[6])
                
                obj=m.Medicine(part[0],part[1],part[2],part[3],float(part[4]),int(part[5]),md,ed,part[8])
                obj.calculate_selling_price()
                self.add_medicine_details(obj)
            except (ex.InvalidMedCodeException,ex.InvalidStockIdException) as e:
                print(e.get_message())
        return None

    def add_medicine_details(self, obj):
        with conn.cursor() as cur:
            q='insert into Medicine values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)'
            l=[obj.get_stock_id(),obj.get_med_code(),obj.get_med_name(),obj.get_category(),obj.get_unit_price(),obj.get_quantity(),obj.get_manufacture_date(),obj.get_expiry_date(),obj.get_status(),obj.get_margin_amount(),obj.get_selling_price(),obj.get_total_stock_value()]
            cur.execute(q,l)
            conn.commit()
            return None

    def find_top3_medicines(self):
        with conn.cursor() as cur:
            cur.execute('select med_code from Medicine')
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            cnt={}
            for c in rows:
                c=c[0]
                if c in cnt:
                    cnt[c]+=1
                else:
                    cnt[c]=1
            
            scnt=dict(sorted(cnt.items(),key=lambda x:x[1],reverse=True))
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
                

    def search_stock(self, stock_id):
        with conn.cursor() as cur:
            q='select * from Medicine where stock_id=:1'
            cur.execute(q,(stock_id,))
            row=cur.fetchone()
            
            if row is None:
                return None
            
            obj=m.Medicine(*row[:9])   
            obj.calculate_selling_price()
            return obj            

    def find_near_expiry(self, ref_date, days_threshold):
        with conn.cursor() as cur:
            q='select stock_id, expiry_date from Medicine where quantity>100 and expiry_date between :1 and :2'
            thd=ref_date+timedelta(days=days_threshold)
            cur.execute(q,(ref_date,thd))
            
            rows=cur.fetchall()
            
            return {id:ed for id,ed in rows}

    def update_unit_price(self, category):
        with conn.cursor() as cur:
            q1="""update Medicine 
            set unit_price=unit_price*1.08
            where category=:1"""
            
            cur.execute(q1,(category,))
            conn.commit()
            
            q2="""update Medicine
            set margin_amount=case
            when category='Tablet' then unit_price*0.12
            when category='Capsule' then unit_price*0.18
            when category='Syrup' then unit_price*0.10
            else unit_price*0.08
            end
            where category=:1"""
            
            cur.execute(q2,(category,))
            conn.commit()
            
            q3="""update Medicine 
            set selling_price=unit_price+margin_amount,
            total_stock_value=unit_price+margin_amount*quantity
            where category=:1"""
            
            cur.execute(q3,(category,))
            conn.commit()
            
            q4="""select * from Medicine
            where category=:1"""
            
            cur.execute(q4,(category,))
            
            rows=cur.fetchall()
            if len(rows)==0:
                return None
            ans=[]
            for r in rows:
                obj=m.Medicine(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
                obj.calculate_selling_price()
                ans.append(obj)
                
            return ans
                
