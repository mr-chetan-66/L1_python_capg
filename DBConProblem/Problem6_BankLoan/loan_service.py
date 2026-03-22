### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import loan_application as la

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class LoanService:

    def __init__(self):
        self.__loan_list = []

    def get_loan_details(self, input_file):
        with conn.cursor() as cur:
            cur.execute('truncate table Loan')
        record=ut.read_file(input_file)
        self.build_loan_list(record)
        return self.__loan_list

    def build_loan_list(self, records):
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_loan_id(part[0])
                ut.validate_loan_type(part[3])
                
                da=ut.convert_date(part[2])
                dd=ut.convert_date(part[4])
                
                obj=la.LoanApplication(part[0],part[1],da,part[3],dd,float(part[5]),int(part[6]),int(part[7]),part[8])
                
                row=self.calculate_loan_costs(float(part[5]),int(part[6]),part[3],int(part[7]))
                
                obj.set_annual_interest_rate(row[0])
                obj.set_processing_fee(row[1])
                obj.set_monthly_emi(row[2])
                obj.set_total_interest(row[3])
                obj.set_total_repayment(row[4])
                
                self.__loan_list.append(obj)
                
            except (ex.InvalidLoanIdException,ex.InvalidLoanTypeException) as e:
                print(e.get_message())  
        return None  

    def calculate_loan_costs(self, loan_amount, tenure_in_months, loan_type, credit_score):
        if loan_type=='Home':
            br,pf=7.0,0.5
        elif loan_type=='Vehicle':
            br,pf=9.0,1.0
        elif loan_type=='Personal':
            br,pf=13.0,2.0
        elif loan_type=='Education':
            br,pf=6.0,0.25
            
        if credit_score>=750:
            ra=-1.5
        elif credit_score>=700:
            ra=-0.75
        elif credit_score>=650:
            ra=0
        else:
            ra=1.0
            
        air=br+ra
        pf=round(loan_amount*(pf/100),2)
        
        r=(air/12)/100
        n=tenure_in_months
        p=loan_amount
        emi=round((p*r*(1+r)**n)/((1+r)**n-1),2)
        tp=round((emi*n),2)
        ti=round((tp-p),2)
        
        return [air,pf,emi,ti,tp]
        
    def add_loan_details(self, loan_list):
        with conn.cursor() as cur:
            for obj in loan_list:
                q='insert into Loan values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)'
                
                l=[obj.get_loan_id(),obj.get_applicant_id(),obj.get_date_of_application(),obj.get_loan_type(),obj.get_date_of_disbursement(),obj.get_loan_amount(),obj.get_tenure_in_months(),obj.get_credit_score(),obj.get_loan_status(),obj.get_annual_interest_rate(),obj.get_processing_fee(),obj.get_monthly_emi(),obj.get_total_interest(),obj.get_total_repayment()]
                
                cur.execute(q,l)
                conn.commit()
            return None    
                

    def search_loan(self, loan_id):
        with conn.cursor() as cur:
            q='select * from Loan where loan_id=:1'
            
            cur.execute(q,(loan_id,))
            
            row=cur.fetchone()
            
            if row is None:
                return None
            obj=la.LoanApplication(*row[:9])
            obj.set_annual_interest_rate(row[9])
            obj.set_processing_fee(row[10])
            obj.set_monthly_emi(row[11])
            obj.set_total_interest(row[12])
            obj.set_total_repayment(row[13])
            return obj

    def update_interest_rate(self, credit_score_threshold):
        with conn.cursor() as cur:
            q1="""update Loan 
            set annual_interest_rate=annual_interest_rate+0.5
            where credit_score<:1""" 
            
            cur.execute(q1,(credit_score_threshold,))
            conn.commit()
            
            q2="""update Loan 
            set monthly_emi=ROUND(
                    (
                        loan_amount
                        *(annual_interest_rate/(12*100))
                        *POWER((1+(annual_interest_rate/(12*100))),tenure_in_months)
                    )
                    /
                    (
                        POWER((1+(annual_interest_rate/(12*100))),tenure_in_months)-1
                    ),2)
                where credit_score<:1""" 
            
            cur.execute(q2,(credit_score_threshold,))
            conn.commit()
            
            q3="""update Loan
            set total_repayment=round(
                (monthly_emi*tenure_in_months)
            ,2)
            where credit_score<:1"""
            
            cur.execute(q3,(credit_score_threshold,))
            conn.commit()
           
            q4="""update Loan
            set total_interest=round(
                (total_repayment-loan_amount)
            ,2)
            where credit_score<:1"""
                
            cur.execute(q4,(credit_score_threshold,))
            conn.commit()

            q5='select * from Loan where credit_score<:1'
            
            cur.execute(q5,(credit_score_threshold,))
            
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            else:
                ans=[]
                for row in rows:
                    obj=la.LoanApplication(*row[:9])
                    obj.set_annual_interest_rate(row[9])
                    obj.set_processing_fee(row[10])
                    obj.set_monthly_emi(row[11])
                    obj.set_total_interest(row[12])
                    obj.set_total_repayment(row[13])
                    ans.append(obj)
                    
                return ans
                    