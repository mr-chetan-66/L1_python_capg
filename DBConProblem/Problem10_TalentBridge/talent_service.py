# Please do not change the skeleton code given here.
import oracledb
import utility as ut
import job_application as jb
import talent_exception as ex

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class TalentService:

    def __init__(self):
        self.__jobObj_lst=[]

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute('truncate table Job')
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_job_code(part[1])
                ut.validate_application_id(part[0])
                
                ad=ut.convert_date(part[5])
                cd=ut.convert_date(part[6])
                
                obj=jb.JobApplication(part[0],part[1],part[2],part[3],int(part[4]),ad,cd,part[7],part[8])
                
                obj.calculate_offered_salary()
                
                self.__jobObj_lst.append(obj)
                
            except (ex.InvalidJobCodeException,ex.InvalidApplicationIdException) as e:
                print(e.get_message()) 
        return self.__jobObj_lst
            

    def add_application_details(self, obj_list):
        with conn.cursor() as cur:
            for obj in obj_list:
                q='insert into Job values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)'
                
                l=[obj.get_application_id(),obj.get_job_code(),obj.get_applicant_name(),obj.get_experience_grade(),obj.get_years_exp(),obj.get_application_date(),obj.get_closing_date(),obj.get_job_title(),obj.get_status(),obj.get_base_salary(),obj.get_experience_bonus(),obj.get_offered_salary()]
                
                cur.execute(q,l)
                conn.commit
        return None

    def find_top3_jobs(self):
        with conn.cursor() as cur:
            q='select job_code,count(*) as cnt from Job group by job_code order by cnt desc'
            
            cur.execute(q)
            
            rows=cur.fetchall()
            ans={}
            i=0
            prev=0
            for jb,cnt in rows:
                if prev!=cnt:
                    i+=1
                    prev=cnt
                if i>3:
                    break
                ans[jb]=cnt
                
            return ans

    def search_application(self, application_id):
        with conn.cursor() as cur:
            q='select * from Job where application_id=:1'
            cur.execute(q,(application_id,))
            row=cur.fetchone()
            
            if row is None:
                return None
            obj=jb.JobApplication(*row[:9])
            obj.calculate_offered_salary()
            return obj

    def find_senior_applicants(self, start_date, end_date):
        with conn.cursor() as cur:
            q='select application_id,years_exp from Job where years_exp>7 and application_date between :1 and :2'
            
            cur.execute(q,(start_date,end_date))
            
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            
            return {id:exp for id,exp in rows}

    def update_offered_salary(self, experience_grade):
        with conn.cursor() as cur:
            q1='update job set offered_salary=offered_salary*1.1,experience_bonus=experience_bonus*1.1 where experience_grade=:1'
            
            cur.execute(q1,(experience_grade,))
            conn.commit()
            
            q2='select * from Job where experience_grade=:1'
            cur.execute(q2,(experience_grade,))
            
            rows=cur.fetchall()
            
            if len(rows)==0:
                return None
            ans=[]
            for row in rows:
                obj=jb.JobApplication(*row[:9])
                obj.calculate_offered_salary()
                obj.set_offered_salary(row[11])
                obj.set_experience_bonus(row[10])
                ans.append(obj)
                
            return ans
            
            
        
