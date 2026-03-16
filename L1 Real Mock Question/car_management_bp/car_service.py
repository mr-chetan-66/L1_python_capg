# Please do not change the skelecton code given here
# You can add any number of methods and attributes as you required without changing the given template
import utility as ut
import car as cr
import sqlite3
from datetime import datetime,timedelta

class CarService:
    
    def __init__(self):
        self.__discount_dict={}
    
    def read_data(self,file_obj):
        for line in file_obj.readlines():
            l=line.split(",")
            cn=l[1]
            if not ut.validate_car_number(cn):
                continue
            obj=cr.Car(l[0],cn,l[2],round(float(l[3]),2),int(l[4]),l[5])
            d=obj.calculate_total_amount()
            
            if d!=0:
                self.__discount_dict[obj.get_rental_id()]=d
            self.add_car_details(obj)
            
    def add_car_details(self,o):
        conn = sqlite3.connect("cardatabase.db")
        cursor = conn.cursor()

        query = """
        INSERT INTO Car (rental_id, car_number, customer_name, basic_cost, no_of_days, rental_date, total_amount)
        VALUES (?,?,?,?,?,?,?)
        """
        l=[o.get_rental_id(),o.get_car_number(),o.get_customer_name(),o.get_basic_cost(),o.get_no_of_days(),o.get_rental_date(),o.get_total_amount()]
        cursor.execute(query,l)
        conn.commit()
        conn.close()
        
    def find_top3_rentals(self):
        conn = sqlite3.connect("cardatabase.db")
        cursor = conn.cursor()

        query = """
            SELECT car_number,COUNT(*) as cnt
            FROM Car 
            GROUP BY car_number
            ORDER BY cnt DESC, car_number ASC
            LIMIT 3
        """
        
        cursor.execute(query)
        f=cursor.fetchall()
        conn.close()
        return {car_num: cnt for (car_num, cnt) in f}
    
    
    def find_closing_date(self,start_date,end_date):
        conn = sqlite3.connect("cardatabase.db")
        cursor = conn.cursor()

        query = """
            SELECT c.rental_id, c.no_of_days, c.rental_date
            FROM Car AS c
            WHERE date(c.rental_date) BETWEEN date(?) AND date(?)
            AND c.car_number IN (
                SELECT car_number
                FROM Car
                GROUP BY car_number
                HAVING COUNT(*) > 3
            )
        """
        l=[start_date,end_date]
        cursor.execute(query,l)
        f=cursor.fetchall()
        
        ans = {}
        for (r_id, days, rental_date_iso) in f:
            d0 = ut.convert_date(rental_date_iso)
            closing = d0 + timedelta(days=int(days))
            ans[r_id] = closing                           # correct: key is rental_id
        return ans

    
    
    
    
   
        
	
