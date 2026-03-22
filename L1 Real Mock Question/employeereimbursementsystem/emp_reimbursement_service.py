### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as you required without changing the given template

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
        # Write your code here
        #list of string -->tuple record
        request=ut.read_file(input_file)
        self.build_emp_reimbursement_list(request)
        return self.__emp_reimbursement_list
    
    def build_emp_reimbursement_list(self, emp_reimburses_records):
        for l in emp_reimburses_records:
            l=l.strip().split(",")
            rid, empcode, dor, grade, dot, nds, lt,ma,*_=l
            if ut.validate_request_id(rid)==True:
                dor=ut.convert_date(dor)
                dot=ut.convert_date(dot)
                nds=int(nds)
                lt=float(lt)
                obj=er.EmpReimbursement(rid,empcode,dor,grade,dot,nds,lt,ma)

                acc_cost, dc, ltc, allow_cost,total=self.calculate_reimbursement_costs(nds,lt,grade)
                obj.set_accomodation_cost(acc_cost)
                obj.set_dining_cost(dc)
                obj.set_local_travel_cost(ltc)
                obj.set_allowances(allow_cost)
                obj.set_total_reimbursement_cost(total)
                self.__emp_reimbursement_list.append(obj)
            else:
                pass
            
        return None
        
    def add_reimbursement_details(self, reimburse_list):
        # Write your code here
        
        with conn.cursor() as cur:
            for obj in reimburse_list:
                query="""INSERT INTO reimbursement
                VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                
                l=[obj.get_request_id(),obj.get_employee_code(),obj.get_date_of_request(),obj.get_grade(),obj.get_date_of_travel(),obj.get_no_of_days_of_stay(),obj.get_local_travel_in_kms(),obj.get_manager_approval(),obj.get_accomodation_cost(),obj.get_dining_cost(),obj.get_allowances(),obj.get_local_travel_cost(),obj.get_total_reimbursement_cost()]
                cur.execute(query,l)
                conn.commit()
        
    def calculate_reimbursement_costs(self,no_of_days, local_kms_travel, grade):
        lvl=int(grade[6:7])
        if lvl in [1,2]:
            ac=10000.0
            dc=1000.0
            ltc=22.0
            allow=1500.0
        elif lvl in [3,4]:
            ac=4000.0
            dc=700.0
            ltc=16.0
            allow=1000.0
        elif lvl in [5,6]:
            ac=2500.0
            dc=450.0
            ltc=12.0
            allow=750.0
            
        ac=ac*no_of_days
        dc=dc*no_of_days
        ltc=ltc*local_kms_travel
        allow=allow*no_of_days
        total=ac+dc+ltc+allow
        
        return [ac,dc,ltc,allow,total]
        
    def search_reimbursement_request(self, request_id):
        
        with conn.cursor() as cur:
            query="""SELECT * FROM reimbursement
            WHERE request_id=:1"""
            
            cur.execute(query,(request_id,))
            
            row=cur.fetchone()
            if row is None:
                return None
            else:
                obj=er.EmpReimbursement(*row[:8])
                obj.set_accomodation_cost(row[8])
                obj.set_dining_cost(row[9])
                obj.set_allowances(row[10])
                obj.set_local_travel_cost(row[11])
                obj.set_total_reimbursement_cost(row[12])
                return obj
        
    def update_costs(self,no_days):
	    # Write your code here
        
        with conn.cursor() as cur:
            
            query="""UPDATE reimbursement
            SET 
                allowances=allowances*(110/100),
                local_travel_cost=local_travel_cost*(110/100)
            WHERE no_of_days_of_stay>:1"""
            
            cur.execute(query,(no_days,))
            conn.commit()
            
            query2="""SELECT * FROM reimbursement
            WHERE no_of_days_of_stay>:1"""
            cur=conn.cursor()
            cur.execute(query2,(no_days,))
            ans=[]
            rows=cur.fetchall()

            for row in rows:
                obj=er.EmpReimbursement(*row[:8])
                obj.set_accomodation_cost(row[8])
                obj.set_allowances(row[10])
                obj.set_dining_cost(row[9])
                obj.set_local_travel_cost(row[11])
                obj.set_total_reimbursement_cost(row[12])
                ans.append(obj)
                    
            return ans
	
	
