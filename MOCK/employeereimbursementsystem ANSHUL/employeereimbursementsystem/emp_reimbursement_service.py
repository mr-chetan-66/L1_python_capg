### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as you required without changing the given template
from datetime import datetime, date, timedelta
import emp_reimbursement as er
import utility as ut
import cx_Oracle
from exception import InvalidRequestIdException
db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
   
#Creating Connection String
conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])



class EmpReimbursementService:
    
    def __init__(self):
        self.__emp_reimbursement_list=[]
    
    def get_emp_reimbursement_details(self, input_file):
        rec_list=ut.read_file(input_file)
        self.build_emp_reimbursement_list(rec_list)
        return self.__emp_reimbursement_list

    def build_emp_reimbursement_list(self, emp_reimburses_records):
        for line in emp_reimburses_records:
            line_list=line.split(",")
            try:
                ut.validate_request_id(line_list[0])
                date_req=ut.convert_date(line_list[2])
                date_travel=ut.convert_date(line_list[4])

                obj = er.EmpReimbursement(line_list[0],line[1],date_req,
                                            line_list[3],date_travel,int(line_list[5]),
                                            float(line_list[6]), line_list[7])

                list_cost=self.calculate_reimbursement_costs(int(line_list[5]),float(line_list[6]),line_list[3])
                obj.set_accomodation_cost(list_cost[0])
                obj.set_dining_cost(list_cost[1])
                obj.set_local_travel_cost(list_cost[2])
                obj.set_allowances(list_cost[3])
                obj.set_total_reimbursement_cost(list_cost[4])
                self.__emp_reimbursement_list.append(obj)

            except InvalidRequestIdException as e:
                print(e)
        
        return
    
    #corretc
    def add_reimbursement_details(self, reimburse_list):
        cursor=conn.cursor()
        for obj in reimburse_list:
            insert="""insert into reimbursement values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
            cursor.execute(insert, (obj.get_request_id(),obj.get_employee_code(),obj.get_date_of_request(),
              obj.get_grade(), obj.get_date_of_travel(), obj.get_no_of_days_of_stay(),
              obj.get_local_travel_in_kms(),obj.get_manager_approval(),obj.get_accomodation_cost(),obj.get_dining_cost(),
              obj.get_allowances(),obj.get_local_travel_cost(),obj.get_total_reimbursement_cost()))
       
        conn.commit()
        return None
    
    #correct
    def calculate_reimbursement_costs(self,no_of_days, local_kms_travel, grade):
        if grade== "Level01":
            acc_cost=10000*no_of_days
            dining_cost=1000*no_of_days
            local_travel_cost=22*local_kms_travel
            allowances=1500*no_of_days
        elif grade== "Level02":
            acc_cost=10000*no_of_days
            dining_cost=1000*no_of_days
            local_travel_cost=22*local_kms_travel
            allowances=1500*no_of_days

        elif grade== "Level03":
            acc_cost=4000*no_of_days
            dining_cost=700*no_of_days
            local_travel_cost=16*local_kms_travel
            allowances=1000*no_of_days
            
        elif grade== "Level04":
            acc_cost=4000*no_of_days
            dining_cost=700*no_of_days
            local_travel_cost=16*local_kms_travel
            allowances=1000*no_of_days
            
        elif grade== "Level05":
            acc_cost=2500*no_of_days
            dining_cost=450*no_of_days
            local_travel_cost=12*local_kms_travel
            allowances=750*no_of_days
            
        elif grade== "Level06":
            acc_cost=2500*no_of_days
            dining_cost=450*no_of_days
            local_travel_cost=12*local_kms_travel
            allowances=750*no_of_days
            
        total_reimbursement_cost=acc_cost+dining_cost+local_travel_cost+allowances

        return [float(acc_cost),float(dining_cost),float(local_travel_cost),float(allowances),float(total_reimbursement_cost)]
    
        
    def search_reimbursement_request(self, request_id):
	    # Write your code here
        cursor=conn.cursor()
        select="""select * from reimbursement where request_id=:1"""
        cursor.execute(select, (request_id,))
        row= cursor.fetchone()
        if row is None:
            return None
        else:
            obj =er.EmpReimbursement(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            obj.set_accomodation_cost(row[8])
            obj.set_dining_cost(row[9])
            obj.set_allowances(row[10])
            obj.set_local_travel_cost(row[11])
            obj.set_total_reimbursement_cost(row[12])
            return obj

	
	#correct
    def update_costs(self,no_days):
        obj_list=[]
        cursor=conn.cursor()
        update="""update reimbursement set 
        allowances=allowances*(110/100), 
        local_travel_cost=local_travel_cost*(110/100),
        total_reimbursement_cost=accomodation_cost+dining_cost+
        allowances+local_travel_cost
        where no_of_days_of_stay>:1"""

        cursor.execute(update, (no_days,))
        conn.commit()
        select="""select * from reimbursement  
        where no_of_days_of_stay>:1"""
        cursor.execute(select,(no_days,))
        rows=cursor.fetchall()
        
        for row in rows:
            obj =er.EmpReimbursement(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            obj.set_accomodation_cost(row[8])
            obj.set_dining_cost(row[9])
            obj.set_allowances(row[10])
            obj.set_local_travel_cost(row[11])
            obj.set_total_reimbursement_cost(row[12])
            obj_list.append(obj)
	    
        return obj_list
	
	
