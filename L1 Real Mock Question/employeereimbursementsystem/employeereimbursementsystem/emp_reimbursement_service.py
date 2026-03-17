### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as you required without changing the given template

import oracledb
import utility as ut
import exception as ex
import emp_reimbursement as em

db=""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}
   
#Creating Connection String
conn=oracledb.connect(user=db['DB_USERNAME'],password=db['DB_PASSWORD'],dsn=db['DSN'])



class EmpReimbursementService:
    
    def __init__(self):
        self.__emp_reimbursement_list=[]
    
    def get_emp_reimbursement_details(self, input_file):
        request=ut.read_file(input_file)
        self.build_emp_reimbursement_list(request)
        return self.__emp_reimbursement_list

    def build_emp_reimbursement_list(self, emp_reimburses_records):
        for line in emp_reimburses_records:
            try:
                row=line.strip().split(",")
                ut.validate_request_id(row[0])
                dor=ut.convert_date(row[2]) 
                dot=ut.convert_date(row[4])
                
                obj=em.EmpReimbursement(row[0],row[1],dor,row[3],dot,int(row[5]),float(row[6]),row[7])
                
                costs=self.calculate_reimbursement_costs(int(row[5]),float(row[6]),row[3])
                
                obj.set_accomodation_cost(costs[0])
                obj.set_dining_cost(costs[1])
                obj.set_local_travel_cost(costs[2])
                obj.set_allowances(costs[3])
                obj.set_total_reimbursement_cost(costs[4])
                
                self.__emp_reimbursement_list.append(obj)
                
            except ex.InvalidRequestIdException as e:
                print(e.get_message())
        
        return None            
    
    
    def add_reimbursement_details(self, reimburse_list):
        with conn.cursor() as cur:
            for obj in reimburse_list:
                
                q="""insert into reimbursement values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                
                l=[obj.get_request_id(),obj.get_employee_code(),obj.get_date_of_request(),obj.get_grade(),obj.get_date_of_travel(),obj.get_no_of_days_of_stay(),obj.get_local_travel_in_kms(),obj.get_manager_approval(),obj.get_accomodation_cost(),obj.get_dining_cost(),obj.get_allowances(),obj.get_local_travel_cost(),obj.get_total_reimbursement_cost()]
                
                cur.execute(q,l)
                conn.commit()
                
        return None

    def calculate_reimbursement_costs(self,no_of_days, local_kms_travel, grade):
        
        lvl=int(grade[6:7])
        
        if lvl in [1,2]:
            ac,dc,lc,alc=10000.0,1000.0,22.0,1500.0
        elif lvl in [3,4]:
            ac,dc,lc,alc=4000.0,700.0,16.0,1000.0
        elif lvl in [5,6]:
            ac,dc,lc,alc=2500.0,450.0,12.0,750.0
            
        ac=ac*no_of_days
        dc=dc*no_of_days
        lc=lc*local_kms_travel
        alc=alc*no_of_days
        total=ac+alc+lc+dc
        
        return [ac,dc,lc,alc,total]
            
    def search_reimbursement_request(self, request_id):
        with conn.cursor() as cur:
            q="""select * from reimbursement where request_id=:1"""
            
            cur.execute(q,(request_id,))

            row=cur.fetchone()
            
            if row is None:
                return None
            
            obj=em.EmpReimbursement(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            obj.set_accomodation_cost(row[8])
            obj.set_dining_cost(row[9])
            obj.set_allowances(row[10])
            obj.set_local_travel_cost(row[11])
            obj.set_total_reimbursement_cost(row[12])
            return obj
        
    def update_costs(self,no_days):
        with conn.cursor() as cur:
            q1="""update reimbursement 
            set allowances=allowances*1.1,
            local_travel_cost=local_travel_cost*1.1,
            total_reimbursement_cost=local_travel_cost+allowances+dining_cost+accomodation_cost
            where no_of_days_of_stay>:1
            """
            cur.execute(q1,(no_days,))
            conn.commit()
            
            q2="""select * from reimbursement where no_of_days_of_stay>:1"""
            
            cur.execute(q2,(no_days,))

            row=cur.fetchall()
            
            if row is None:
                return None
            ans=[]
            for obj in row:
                sobj=em.EmpReimbursement(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],obj[7])
                sobj.set_accomodation_cost(obj[8])
                sobj.set_dining_cost(obj[9])
                sobj.set_allowances(obj[10])
                sobj.set_local_travel_cost(obj[11])
                sobj.set_total_reimbursement_cost(obj[12])
                ans.append(sobj)
            return ans            
	
	
