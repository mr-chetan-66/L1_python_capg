### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import patient_billing as pb

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

# Creating Connection
conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class PatientBillingService:

    def __init__(self):
        self.__patient_billing_list = []

    def get_patient_billing_details(self, input_file):
        with conn.cursor() as cur:
            cur.execute('truncate table Bill')
        record=ut.read_file(input_file)
        self.build_patient_billing_list(record)
        return self.__patient_billing_list

    def build_patient_billing_list(self, records):
        
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_bill_id(part[0])
                ut.validate_ward_type(part[3])
                
                da=ut.convert_date(part[2])
                dd=ut.convert_date(part[4])
                
                obj=pb.PatientBilling(part[0],part[1],da,part[3],dd,int(part[5]),part[6],part[7])
                
                row=self.calculate_billing_costs(int(part[5]),part[3])
                obj.set_bed_charges(row[0])
                obj.set_treatment_charges(row[1])
                obj.set_nursing_charges(row[2])
                obj.set_discount(row[3])
                obj.set_total_bill_amount(row[4])
                
                self.__patient_billing_list.append(obj)
                
            except (ex.InvalidBillIdException,ex.InvalidWardTypeException) as e:
                print(e.get_message())
        return None

    def calculate_billing_costs(self, no_of_days, ward_type):
        if ward_type=='General':
            bc,tc,nc,d=500.0,800.0,300.0,5
        elif ward_type=='Semi-Private':
            bc,tc,nc,d=1500.0,1500.0,600.0,3
        elif ward_type=='Private':
            bc,tc,nc,d=3000.0,2500.0,1000.0,2
        elif ward_type=='ICU':
            bc,tc,nc,d=8000.0,5000.0,2000.0,0
            
        bc=bc*no_of_days
        tc=tc*no_of_days
        nc=nc*no_of_days
        gt=bc+nc+tc
        d=gt*(d/100)
        total=gt-d
        
        return [bc,tc,nc,d,total]

    def add_billing_details(self, billing_list):
        with conn.cursor() as cur:
            for obj in billing_list:
                q='insert into Bill values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)'
            
                l=[obj.get_bill_id(),obj.get_patient_id(),obj.get_date_of_admission(),obj.get_ward_type(),obj.get_date_of_discharge(),obj.get_no_of_days(),obj.get_treatment_code(),obj.get_insurance_status(),obj.get_bed_charges(),obj.get_treatment_charges(),obj.get_nursing_charges(),obj.get_discount(),obj.get_total_bill_amount()]
            
                cur.execute(q,l)
                print(f"Inserted: {obj.get_bill_id()}")
                conn.commit()
                
        return None

    def search_billing_record(self, bill_id):
        with conn.cursor() as cur:
            q='select * from Bill where bill_id=:1'
            cur.execute(q,(bill_id,))
            row=cur.fetchone()
            
            if row is None:
                return None
            obj=pb.PatientBilling(*row[:8])
            obj.set_bed_charges(row[8])
            obj.set_treatment_charges(row[9])
            obj.set_nursing_charges(row[10])
            obj.set_discount(row[11])
            obj.set_total_bill_amount(row[12])
            return obj

    def update_charges(self, no_days):
        with conn.cursor() as cur:
            q1="""update Bill 
            set  bed_charges=bed_charges*1.15,
            nursing_charges=nursing_charges*1.15
            where no_of_days>:1"""
            
            cur.execute(q1,(no_days,))
            conn.commit()
            
            q2="""update Bill set
            discount=case
            when ward_type='General' then (bed_charges+nursing_charges+treatment_charges)*0.05
            when ward_type='Semi-Private' then (bed_charges+nursing_charges+treatment_charges)*0.03
            when ward_type='Private' then (bed_charges+nursing_charges+treatment_charges)*0.02
            when ward_type='ICU' then 0
            end
            where no_of_days>:1"""
            
            cur.execute(q2,(no_days,))
            conn.commit()
            
            q3="""update Bill set total_bill_amount=(bed_charges+nursing_charges+treatment_charges)-discount 
            where no_of_days>:1"""
            cur.execute(q3,(no_days,))
            conn.commit()
            
            q4="select * from Bill where no_of_days>:1"
            
            cur.execute(q4,(no_days,))
            
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            else:
                ans=[]
                for row in rows:
                    obj=pb.PatientBilling(*row[:8])
                    obj.set_bed_charges(row[8])
                    obj.set_treatment_charges(row[9])
                    obj.set_nursing_charges(row[10])
                    obj.set_discount(row[11])
                    obj.set_total_bill_amount(row[12])
                    ans.append(obj)
                return ans
