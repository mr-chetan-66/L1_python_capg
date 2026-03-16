### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as you required without changing the given template

import emp_reimbursement as er
import utility as ut
import oracledb
from exception import InvalidRequestIdException

# db=""
# with open('database.properties') as f:
#     lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
#     db = {key.strip(): value.strip() for key, value in lines}
   
# #Creating Connection String
# conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])

conn  = oracledb.connect(
            user="system",
            password="12345",
            dsn = oracledb.makedsn("10.110.182.9", 1521, sid="XE")
        )
cursor = conn.cursor()
query="""CREATE TABLE reimbursement (
    request_id                VARCHAR2(100),
    employee_code             VARCHAR2(100),
    date_of_request           DATE,
    grade                     VARCHAR2(50),
    date_of_travel            DATE,
    no_of_days_of_stay        NUMBER,
    local_travel_in_kms       NUMBER(10,2),
    manager_approval          VARCHAR2(50),
    accomodation_cost         NUMBER(12,2),
    dining_cost               NUMBER(12,2),
    allowances                NUMBER(12,2),
    local_travel_cost         NUMBER(12,2),
    total_reimbursement_cost  NUMBER(12,2)
)"""
cursor.execute(query)
conn.commit()
print("done")

# class EmpReimbursementService:
    
#     def __init__(self):
#         self.__emp_reimbursement_list=[]
       
#     # no need
#     # def get_emp_reimbursement_list(self):
#     #     return self.__emp_reimbursement_list
    
    
#     def get_emp_reimbursement_details(self, input_file):
#         # Write your code here
#         #list of string -->tuple record
#         request=ut.read_file(input_file)
#         self.build_emp_reimbursement_list(request)
#         return self.__emp_reimbursement_list
    
#     def build_emp_reimbursement_list(self, emp_reimburses_records):
#         for l in emp_reimburses_records:
#             l=l.split(",")
#             rid, empcode, dor, grade, dot, nds, lt,ma,*_=l
#             try:
#                 if ut.validate_request_id(rid):
#                     dor=ut.convert_date(dor)
#                     dot=ut.convert_date(dot)
#                     nds=int(nds)
#                     lt=round(float(lt),1)
#                     obj=er.EmpReimbursement(rid,empcode,dor,grade,dot,nds,lt,ma)

#                     acc_cost, dc, ltc, allow_cost,total=self.calculate_reimbursement_costs(nds,lt,grade)
#                     obj.set_accomodation_cost(acc_cost)
#                     obj.set_dining_cost(dc)
#                     obj.set_local_travel_cost(ltc)
#                     obj.set_allowances(allow_cost)
#                     obj.set_total_reimbursement_cost(total)
#                     self.__emp_reimbursement_list.append(obj)
#             except InvalidRequestIdException as e:
#                 print(e.get_message()) #get no ned
        
#     def add_reimbursement_details(self, reimburse_list):
#         # Write your code here
#         conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
#         cur=conn.cursor()
        
#         for obj in reimburse_list:
#             #check column name
#             query="""INSERT INTO reimbursement(request_id, employee_code, date_of_request, grade, date_of_travel, no_of_days_of_stay, local_travel_in_kms,manager_approval,accomodation_cost,dining_cost,allowances,total_reimbursement_cost,local_travel_cost)
#             VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
            
#             l=[obj.get_request_id(),obj.get_employee_code(),obj.get_date_of_request(),obj.get_grade(),obj.get_date_of_travel(),obj.get_no_of_days_of_stay(),obj.get_local_travel_in_kms(),obj.get_manager_approval(),obj.get_accomodation_cost(),obj.get_dining_cost(),obj.get_allowances(),obj.get_local_travel_cost(),obj.get_total_reimbursement_cost()]
#             cur.execute(query,l)
            
#         conn.commit()
#         cur.close()
#         conn.close()
#         #return None
    
#     def calculate_reimbursement_costs(self,no_of_days, local_kms_travel, grade):
#         lvl=int(grade[6])
#         ac=0.0
#         dc=0.0
#         ltc=0.0
#         allow=0.0
#         if lvl in [1,2]:
#             ac=10000.0
#             dc=1000.0
#             ltc=22.0
#             allow=1500.0
#         elif lvl in [3,4]:
#             ac=4000.0,
#             dc=700.0
#             ltc=16.0
#             allow=1000.0
#         elif lvl in [5,6]:
#             ac=2500.0
#             dc=450.0
#             ltc=12.0
#             allow=750.0
            
#         ac=round(ac*no_of_days,1)
#         dc=round(dc*no_of_days,1)
#         ltc=round(ltc*local_kms_travel,1)
#         allow=round(allow*no_of_days,1)
#         total=round(ac+dc+ltc+allow,1)
        
#         return [ac,dc,ltc,allow,total]
        
#     def search_reimbursement_request(self, request_id):
#         conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
#         cur=conn.cursor()
#         query="""SELECT * FROM reimbursement
#         WHERE LOWER(request_id)=LOWER(:1)"""
        
#         cur.execute(query,(request_id,))
        
#         row=cur.fetchone()
#         if row is None:
#             return None
#         else:
#             #when we fetch from database we dont need to convert into specific datatype it done automatically
#             dor=ut.convert_date(row[2])
#             dot=ut.convert_date(row[4])
#             nds=int(row[5])
#             lt=round(float(row[6]),1)
#             acc=round(float(row[6]),1)
#             dc=round(float(row[6]),1)
#             all=round(float(row[6]),1)
#             ltc=round(float(row[6]),1)
#             total=round(float(row[6]),1)
            
#             obj=er.EmpReimbursement(row[0],row[1],dor,row[3],dot,nds,lt,row[7])
#             obj.set_accomodation_cost(acc)
#             obj.set_allowances(all)
#             obj.set_dining_cost(dc)
#             obj.set_local_travel_cost(ltc)
#             obj.set_total_reimbursement_cost(total)
#             cur.close()
#             conn.close()
#             return obj
        
	
	
#     def update_costs(self,no_days):
# 	    # Write your code here
#         conn=cx_Oracle.connect(db['DB_USERNAME'],db['DB_PASSWORD'],db['DSN'])
#         cur=conn.cursor()
#         query="""UPDATE reimbursement
#         SET 
#             allowances=allowances*1.1                 >>#comma miss
#             local_travel_cost=local_travel_cost*1.1   >>##total cost missing need to update that also after allowncance change
#         WHERE no_of_days_of_stay>:1"""
        
#         cur.execute(query,(no_days,))
#         conn.commit()
        
#         query2="""SELECT * FROM reimbursement
#         WHERE no_of_days_of_stay>:1"""

#         cur.execute(query2,(no_days,))
#         ans=[]
#         rows=cur.fetchall()
#         if rows is None:
#             return None
#         else:
#             for row in rows:
#                 dor=ut.convert_date(row[2])
#                 dot=ut.convert_date(row[4])
#                 nds=int(row[5])
#                 lt=round(float(row[6]),1)
#                 acc=round(float(row[6]),1)
#                 dc=round(float(row[6]),1)
#                 all=round(float(row[6]),1)
#                 ltc=round(float(row[6]),1)
#                 total=round(float(row[6]),1) #no need
            
#                 obj=er.EmpReimbursement(row[0],row[1],dor,row[3],dot,nds,lt,row[7])
#                 obj.set_accomodation_cost(acc)
#                 obj.set_allowances(all)
#                 obj.set_dining_cost(dc)
#                 obj.set_local_travel_cost(ltc)
#                 obj.set_total_reimbursement_cost(total)
#                 ans.append(obj)
                
#         cur.close()
#         conn.close()
#         return ans
	
	
