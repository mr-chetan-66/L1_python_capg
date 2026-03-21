### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import shipment_order as so

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class ShipmentService:

    def __init__(self):
        self.__shipment_list = []

    def get_shipment_details(self, input_file):
        with conn.cursor() as cur:
            cur.execute('truncate table ShipOrder')
        record=ut.read_file(input_file)
        self.build_shipment_list(record)
        return self.__shipment_list

    def build_shipment_list(self, records):
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_shipment_id(part[0])
                ut.validate_zone(part[3])
                dp=ut.convert_date(part[2])
                dd=ut.convert_date(part[4])
                obj=so.ShipmentOrder(part[0],part[1],dp,part[3],dd,float(part[5]),part[6],part[7])
                
                row=self.calculate_shipping_costs(float(part[5]),part[3],dp,dd)
                
                obj.set_freight_charge(row[0])
                obj.set_handling_charge(row[1])
                obj.set_delay_penalty(row[2])
                obj.set_tax(row[3])
                obj.set_total_shipping_cost(row[4])
                self.__shipment_list.append(obj)
            except (ex.InvalidShipmentIdException,ex.InvalidZoneException) as e:
                print(e.get_message())
        return None
            

    def calculate_shipping_costs(self, weight_in_kg, zone, date_of_dispatch, date_of_delivery):
        if zone=='Zone_A':
            f,h,t=50.0,10.0,5
        elif zone=='Zone_B':
            f,h,t=80.0,15.0,8
        elif zone=='Zone_C':
            f,h,t=120.0,20.0,10
        elif zone=='Zone_D':
            f,h,t=200.0,30.0,12
            
        dp=0 
        if ((date_of_delivery-date_of_dispatch).days)>7:
            dp=25*weight_in_kg
        f*=weight_in_kg
        h*=weight_in_kg
        gr=f+h
        tax=gr*(t/100)
        
        total=gr+tax+dp
        
        return [f,h,dp,tax,total]
        
    def add_shipment_details(self, shipment_list):
        with conn.cursor() as cur:
            q='insert into ShipOrder values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)'
            for obj in shipment_list:
                
                l=[obj.get_shipment_id(),obj.get_sender_id(),obj.get_date_of_dispatch(),obj.get_zone(),obj.get_date_of_delivery(),obj.get_weight_in_kg(),obj.get_shipment_type(),obj.get_delivery_status(),obj.get_freight_charge(),obj.get_handling_charge(),obj.get_delay_penalty(),obj.get_tax(),obj.get_total_shipping_cost()]
                
                cur.execute(q,l)
                conn.commit()
                
        return None

    def search_shipment(self, shipment_id):
        with conn.cursor() as cur:
            q='select * from ShipOrder where shipment_id=:1'
            cur.execute(q,(shipment_id,))
            
            row=cur.fetchone()
            
            if row is None:
                return None
            obj=so.ShipmentOrder(*row[:8])
            obj.set_freight_charge(row[8])
            obj.set_handling_charge(row[9])
            obj.set_delay_penalty(row[10])
            obj.set_tax(row[11])
            obj.set_total_shipping_cost(row[12])
            return obj

    def update_freight(self, weight_threshold):
        with conn.cursor() as cur:
            q1="""update ShipOrder
            set freight_charge=freight_charge*1.2
            where weight_in_kg>:1"""
            
            cur.execute(q1,(weight_threshold,))
            conn.commit()
            
            q2="""update ShipOrder
            set tax=case
            when zone='Zone_A' then (freight_charge+handling_charge)*0.05
            when zone='Zone_B' then (freight_charge+handling_charge)*0.08
            when zone='Zone_C' then (freight_charge+handling_charge)*0.1
            when zone='Zone_D' then (freight_charge+handling_charge)*0.12
            end 
            where weight_in_kg>:1
            """
            
            cur.execute(q2,(weight_threshold,))
            conn.commit()
            
            q3="""update ShipOrder
            set total_shipping_cost=tax+(freight_charge+handling_charge)+delay_penalty
            where weight_in_kg>:1
            """
            cur.execute(q3,(weight_threshold,))
            conn.commit()
            
            q4='select * from ShipOrder where weight_in_kg>:1'
            
            cur.execute(q4,(weight_threshold,))
            
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None  
            ans=[]
            for row in rows:
                obj=so.ShipmentOrder(*row[:8])
                obj.set_freight_charge(row[8])
                obj.set_handling_charge(row[9])
                obj.set_delay_penalty(row[10])
                obj.set_tax(row[11])
                obj.set_total_shipping_cost(row[12])
                ans.append(obj)
            return ans
                            
