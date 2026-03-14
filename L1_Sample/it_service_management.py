# it_service_management.py
import it_service as its
import utility as ut
import sqlite3

## Creating Connection String
# (We will NOT rely on this global conn; we will open/close inside methods to satisfy resource-closing constraint)
conn = sqlite3.connect("database_table.db")

class ITServiceManagement:
    
    def __init__(self):
        self.__service_list=[]     
     
    def get_service_list(self):
        return self.__service_list

    def set_service_list(self, service_list):
        self.__service_list = service_list

    def build_service_details(self, service_data):
        ## Write your code here
        # service_data: list of lists [service_id, customer_name, date_str, service_type, base_charge_str]
        for rec in service_data:
            try:
                service_id, customer_name, date_str, service_type, base_str = rec
                # Validate ID
                ut.validate_service_id(service_id)
                # Convert date
                service_date = ut.convert_date(date_str)
                # Parse base charge
                base_charge = float(base_str)
                # Create object
                it_obj = its.ITService(service_id, customer_name, service_date, service_type, base_charge)
                # Compute charges
                it_obj.calculate_service_charge()
                # Append to list
                self.__service_list.append(it_obj)
            except Exception:
                # Skip malformed/invalid records (as per spec: append only valid ones)
                continue
            
    def add_service_details(self):
        ## Write your code here
        # Insert all objects in self.__service_list into 'service' table
        con = sqlite3.connect("database_table.db")
        try:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS service (
                    service_id TEXT,
                    customer_name TEXT,
                    service_date TEXT,
                    service_type TEXT,
                    base_charge REAL,
                    service_charge REAL
                )
            """)
            # Insert each service
            for obj in self.__service_list:
                cur.execute("""
                    INSERT INTO service (service_id, customer_name, service_date, service_type, base_charge, service_charge)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    obj.get_service_id(),
                    obj.get_customer_name(),
                    obj.get_service_date().isoformat(),
                    obj.get_service_type(),
                    obj.get_base_charge(),
                    obj.get_service_charge()
                ))
            con.commit()
        finally:
            cur.close()
            con.close()
        
    def search_service_id(self, service_id):
        ## Write your code here
        con = sqlite3.connect("database_table.db")
        try:
            cur = con.cursor()
            cur.execute("""
                SELECT service_id, customer_name, service_date, service_type, base_charge, service_charge
                FROM service WHERE service_id = ?
            """, (service_id,))
            row = cur.fetchone()
            if not row:
                return None
            sid, name, date_str, s_type, base, charge = row
            # Recreate the ITService object
            date_obj = ut.convert_date(date_str)
            obj = its.ITService(sid, name, date_obj, s_type, float(base))
            obj.set_service_charge(float(charge))
            return obj
        finally:
            cur.close()
            con.close()