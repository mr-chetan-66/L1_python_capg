# Please do not change the skelecton code given here
# You can add any number of methods and attributes as you required without changing the given template
import utility as ut
import car as cr
import cx_Oracle
from datetime import date, timedelta

##import necessary modules/packages here

db = ""
with open("database.properties") as f:
    lines = [
        line.strip().split("=")
        for line in f.readlines()
        if not line.startswith("#") and line.strip()
    ]
    db = {key.strip(): value.strip() for key, value in lines}

##Creating Connection String

class CarService:

    def __init__(self):
        self.__discount_dict = {}

    def read_data(self, file_obj):
        for line in file_obj:
            info = line.strip().split(",")
            car_number = info[1]
            
            if ut.validate_car_number(car_number):
                str_date = info[5]
                rental_date = ut.convert_date(str_date)
                basic_cost = info[3]
                no_of_days = info[4]
                obj = cr.Car(
                    info[0],
                    info[1],
                    info[2],
                    float(basic_cost),
                    int(no_of_days),
                    rental_date,
                )
                dis=obj.calculate_total_amount()
                self.add_car_details(obj)
                if obj.get_no_of_days()>1:
                    self.__discount_dict[obj.get_rental_id]=dis

    def add_car_details(self, car_obj):
        query = """
            INSERT INTO Car (rental_id,car_number,customer_name,basic_cost,no_of_days,rental_date,total_amount)
            VALUES (:1,:2,:3,:4,:5,:6,:7)
        """
        conn = cx_Oracle.connect(db["DB_USERNAME"], db["DB_PASSWORD"], db["DSN"])
        cur = conn.cursor()
        l = (car_obj.get_rental_id(),car_obj.get_car_number(),car_obj.get_customer_name(),car_obj.get_basic_cost(),car_obj.get_no_of_days(),car_obj.get_rental_date(),car_obj.get_total_amount())

        cur.execute(query, l)
        conn.commit()
        cur.close()
        conn.close()

        return  ##TODO: RETURN VALUE AS PER THE DESCRIPTION

    def find_top3_rentals(self):
        # Write your code

        query = """WITH freq AS (
            SELECT car_number,COUNT(*) AS count
            FROM Car
            GROUP BY car_number
            ),
            ranked AS (
                SELECT car_number,cnt,
                DENSE RANK() OVER (ORDER BY cnt DESC) AS rnk
                FROM freq
            )
            SELECT * FROM ranked
            WHERE rnk<=3 
            """
        conn = cx_Oracle.connect(db["DB_USERNAME"], db["DB_PASSWORD"], db["DSN"])
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        top={}
        for row in rows:
            top[row[0]]=row[1]
            
        cur.close()
        conn.close()
        return top  ##TODO: RETURN VALUE AS PER THE DESCRIPTION

    def find_closing_date(self, start_date, end_date):
        # Write your code
        query = "SELECT * FROM Car WHERE no_of_days>3 AND rental_date BETWEEN :1 AND :2"
        conn = cx_Oracle.connect(db["DB_USERNAME"], db["DB_PASSWORD"], db["DSN"])
        cursor = conn.cursor()
        cursor.execute(query,(start_date,end_date))
        rows = cursor.fetchall()
        cursor.close()
        resDict = {}
        for row in rows:
            d=row[5]
            nd=row[4]
            d=d+timedelta(days=nd)
            resDict[row[0]]=d
        return resDict  ##TODO: RETURN VALUE AS PER THE DESCRIPTION
