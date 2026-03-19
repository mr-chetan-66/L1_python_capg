## Please do not change the skelecton code given here. Write your code only in the provided places alone.

import it_service as its
import utility as ut
import cx_Oracle

db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
   
## Creating Connection String
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
cursor=conn.cursor()



class ITServiceManagement:
    
    def __init__(self):
        self.__service_list = []
        
    def get_service_list(self):
        return self.__service_list

    def set_service_list(self, service_list):
        self.__service_list = service_list
        
    def build_service_details(self, service_data):
        ## Write your code here
        for val in service_data:
            valid = ut.validate_service_id(val[0])
            if valid == True:
                convertedDate = ut.convert_date(val[2])
                obj = its.ITService(val[0], val[1], convertedDate, val[3], float(val[4]))
                obj.calculate_service_charge()
                self.__service_list.append(obj)
    
    def add_service_details(self):
        ## Write your code here
        sql = """
            INSERT INTO service VALUES 
            (:1, :2, :3, :4, :5, :6)
        """
        lst = []
        for vals in self.__service_list:
            lst.append((vals.get_service_id(), vals.get_customer_name(), vals.get_service_date(), vals.get_service_type(), vals.get_base_charge(), vals.get_service_charge()))
        cursor.executemany(sql, lst)
        conn.commit()
        
    def search_service_id(self, service_id):
        ## Write your code here
        sql ="""
            SELECT * FROM service WHERE service_id = :1
        """
        cursor.execute(sql, [service_id])
        val = cursor.fetchone()
        if val is None:
            return None
        obj = its.ITService(val[0], val[1], val[2], val[3], float(val[4]))
        obj.set_service_charge(val[5])
        return obj    
	
	
               
        