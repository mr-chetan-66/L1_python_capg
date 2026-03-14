## Please do not change the skelecton code given here. Write your code only in the provided places alone.

import it_service as its
import utility as ut
import sqlite3

## Creating Connection String
conn = sqlite3.connect("database_table.db")



class ITServiceManagement:
    
    def __init__(self):
        self.__service_list = []
    
    
    def get_service_list(self):
        return self.__service_list

    def set_service_list(self, service_list):
        self.__service_list = service_list 

    def build_service_details(self, service_data):
        ## Write your code here
        for data in service_data:
            service_id = data[0]
            customer_name = data[1]
            service_date = data[2]
            service_type = data[3]
            base_charge= data[4]
            
            ut.validate_service_id(service_id)
            date_obj = ut.convert_date(service_date)
            it_obj = its.ITService(service_id,customer_name,date_obj,service_type,base_charge)
            it_obj.calculate_service_charge()
            self.__service_list.append(it_obj)
        
    
    def add_service_details(self):
        ## Write your code here
        cur = conn.cursor()
        query = """INSERT OR IGNORE INTO service VALUES(?,?,?,?,?,?)"""
        for obj in self.__service_list:
            cur.execute(query,(obj.get_service_id(),obj.get_customer_name(),str(obj.get_service_date()),obj.get_service_type(),obj.get_base_charge(),obj.get_service_charge(),))
            conn.commit()
        
        
    def search_service_id(self, service_id):
        ## Write your code here
        cur = conn.cursor()
        query = """SELECT * FROM service WHERE service_id=?"""
        cur.execute(query,(service_id,))
        row = cur.fetchone()
        if row:
            
            its_obj = its.ITService(row[0],row[1],row[2],row[3],row[4])
            its_obj.set_service_charge(row[5])
            return its_obj
        else :
            return None

