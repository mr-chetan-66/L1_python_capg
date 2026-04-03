# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import hotel_booking as hb
import hotel_exception as ex
from datetime import timedelta

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class HotelService:

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("truncate table HotelBooking")
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_booking_id(part[0])
                ut.validate_room_number(part[1])
                dob=ut.convert_date(part[8])
                doc=ut.convert_date(part[5])
                obj=hb.HotelBooking(part[0],part[1],part[2],float(part[3]),int(part[4]),doc,part[6],part[7],dob)
                obj.calculate_all_amount()
                self.add_booking_details(obj)
            except ex.InvalidBookingIdException as e:
                print(e.get_message())
            except ex.InvalidRoomNumberException as e:
                print(e.get_message())
            
        return None

    def add_booking_details(self, obj):
        with conn.cursor() as cur:
            q='insert into HotelBooking values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)'
            
            l=[obj.get_booking_id(),
                obj.get_room_number(),
                obj.get_guest_name(),
                obj.get_room_rate(),
                obj.get_no_of_nights(),
                obj.get_check_in_date(),
                obj.get_room_type(),
                obj.get_status(),
                obj.get_booking_date(),
                obj.get_base_amount(),
                obj.get_tax_amount(),
                obj.get_total_amount()]
            
            cur.execute(q,l)
            # print(cur.rowcount)
            conn.commit()

    def find_top3_rooms(self):
        with conn.cursor() as cur:
            q='select room_number from HotelBooking'
            cur.execute(q)
            rows=cur.fetchall()
            cnt={}
            for rn in rows:
                rn=rn[0]
                if rn in cnt:
                    cnt[rn]+=1
                else:
                    cnt[rn]=1
            
            sort_cnt=dict(sorted(cnt.items(), key=lambda x:x[1],reverse=True))
            
            i=0
            prev=0
            ans={}
            for k,v in sort_cnt.items():
                if prev!=v:
                    prev=v
                    i+=1
                if i>3:
                    break
                ans[k]=v
            return ans

    def search_booking(self, booking_id):
        with conn.cursor() as cur:
            q='select * from HotelBooking where booking_id=:1'
            cur.execute(q,(booking_id,))
            row=cur.fetchone()
            
            if row is None:
                return None
            else:
                obj=hb.HotelBooking(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                obj.calculate_all_amount()
                return obj

    def find_checkout_dates(self, start_date, end_date):
        with conn.cursor() as cur:
            q='select booking_id,check_in_date,no_of_nights from HotelBooking where no_of_nights>5 and check_in_date between :1 and :2'
            
            cur.execute(q,(start_date,end_date))
            
            rows=cur.fetchall()
            
            return {id:(d+timedelta(days=nd)) for id,d,nd in rows}

    def update_tax_rates(self, room_type):
        with conn.cursor() as cur:
            q='update HotelBooking set tax_amount=tax_amount*1.1,total_amount=base_amount+tax_amount where room_type=:1'
            
            cur.execute(q,(room_type,))
            conn.commit()
            q1='select * from HotelBooking where room_type=:1'
            
            cur.execute(q1,(room_type,))
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            ans=[]
            for r in rows:
                obj=hb.HotelBooking(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
                obj.calculate_all_amount()
                ans.append(obj)
                
            return ans
                
                
