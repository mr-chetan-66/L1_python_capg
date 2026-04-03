### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import scholarship_application as sa

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class ScholarshipService:

    def __init__(self):
        self.__scholarship_list = []

    def get_scholarship_details(self, input_file):
        with conn.cursor() as cur:
            cur.execute('truncate table Scholarship')
        record=ut.read_file(input_file)
        self.build_scholarship_list(record)
        return self.__scholarship_list

    def build_scholarship_list(self, records):
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_application_id(part[0])
                ut.validate_course_type(part[3])
                
                da=ut.convert_date(part[2])
                de=ut.convert_date(part[4])
                
                obj=sa.ScholarshipApplication(part[0],part[1],da,part[3],de,float(part[5]),float(part[6]),part[7],part[8])
                
                row=self.calculate_scholarship(part[3],float(part[5]),float(part[6]),part[7])
                
                obj.set_base_scholarship(row[0])
                obj.set_merit_bonus(row[1])
                obj.set_income_waiver(row[2])
                obj.set_total_scholarship(row[3])
                
                self.__scholarship_list.append(obj)
            except (ex.InvalidApplicationIdException,ex.InvalidCourseTypeException) as e:
                print(e.get_message())
        return None

    def calculate_scholarship(self, course_type, cgpa, annual_family_income, category):
        if course_type=='UG':
            bs=40000.0
        elif course_type=='PG':
            bs=60000.0
        elif course_type=='Diploma':
            bs=25000.0
        elif course_type=='PhD':
            bs=100000.0
        
        mb=0
        if cgpa>=9.0:
            mb=25
        elif cgpa>=8.0:
            mb=15
        elif cgpa>=8.0:
            mb=25
            
        mb=bs*(mb/100)
        
        if annual_family_income>=500000.0:
            iw=0
        elif annual_family_income>=250000.0:
            iw=3000.0
        elif annual_family_income>=100000.0:
            iw=8000.0
        else:
            iw=15000.0
            
        if category=='SC':
            mul=1.20
        elif category=='ST':
            mul=1.25
        elif category=='OBC':
            mul=1.10
        elif category=='General':
            mul=1.00
            
        ts=round((bs+mb+iw)*mul,2)
        
        return [bs,mb,iw,ts]
        
    def add_scholarship_details(self, scholarship_list):
        with conn.cursor() as cur:
            q='insert into Scholarship values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)'
            for obj in scholarship_list:
                
                l=[obj.get_application_id(),obj.get_student_id(),obj.get_date_of_application(),obj.get_course_type(),obj.get_date_of_enrollment(),obj.get_cgpa(),obj.get_annual_family_income(),obj.get_category(),obj.get_application_status(),obj.get_base_scholarship(),obj.get_merit_bonus(),obj.get_income_waiver(),obj.get_total_scholarship()]
                
                cur.execute(q,l)
                conn.commit()
                
            return None

    def search_application(self, application_id):
        with conn.cursor() as cur:
            q='select * from Scholarship where application_id=:1'
            
            cur.execute(q,(application_id,))
            
            row=cur.fetchone()
            
            if row is None:
                return None
            
            obj=sa.ScholarshipApplication(*row[:9])
            obj.set_base_scholarship(row[9])
            obj.set_merit_bonus(row[10])
            obj.set_income_waiver(row[11])
            obj.set_total_scholarship(row[12])
            return obj

    def update_merit_bonus(self, cgpa_threshold):
        with conn.cursor() as cur:
            q1="""update Scholarship
            set merit_bonus=merit_bonus*1.1
            where cgpa>:1"""
            
            cur.execute(q1,(cgpa_threshold,))
            conn.commit()
            
            q2="""update Scholarship
            set total_scholarship=(base_scholarship+merit_bonus+income_waiver)*case
            when category='SC' then 1.20
            when category='ST' then 1.25
            when category='OBC' then 1.10
            when category='General' then 1.0
            end
            where cgpa>:1"""
            
            cur.execute(q2,(cgpa_threshold,))
            conn.commit()
            
            q3='select * from Scholarship where cgpa>:1'
            
            cur.execute(q3,(cgpa_threshold,))
            
            rows=cur.fetchall()
            
            if not rows:
                return None
            ans=[]
            for row in rows:
                obj=sa.ScholarshipApplication(*row[:9])
                obj.set_base_scholarship(row[9])
                obj.set_merit_bonus(row[10])
                obj.set_income_waiver(row[11])
                obj.set_total_scholarship(row[12])
                ans.append(obj)
                
            return ans