import utility as ut
import job_application as ja
import oracledb
import talent_exception as te

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])

class TalentService:
    def __init__(self):
        self.__bonus_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE JobApplication")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_job_code(part[1])
                ut.validate_application_id(part[0])
                apd = ut.convert_date(part[5]); cld = ut.convert_date(part[6])
                obj = ja.JobApplication(part[0], part[1], part[2], part[3], int(part[4]), apd, cld, part[7])
                bonus = obj.calculate_offered_salary()
                self.add_application_details(obj)
                self.__bonus_dict[obj.get_application_id()] = bonus
            except te.InvalidJobCodeException as e: print(e.get_message())
            except te.InvalidApplicationIdException as e: print(e.get_message())
        return None

    def add_application_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into JobApplication values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
            cur.execute(q, [obj.get_application_id(), obj.get_job_code(), obj.get_applicant_name(),
                            obj.get_experience_grade(), obj.get_years_exp(),
                            obj.get_application_date(), obj.get_closing_date(), obj.get_job_title(),
                            obj.get_base_salary(), obj.get_experience_bonus(), obj.get_offered_salary()])
            conn.commit()
        return None

    def find_top3_jobs(self):
        with conn.cursor() as cur:
            cur.execute("select * from JobApplication")
            freq = {}
            for row in cur.fetchall(): freq[row[1]] = freq.get(row[1], 0) + 1
            sorted_f = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}; i = prev = 0
            for k, v in sorted_f.items():
                if v != prev: prev = v; i += 1
                if i > 3: break
                res[k] = v
            return res

    def search_application(self, application_id):
        with conn.cursor() as cur:
            cur.execute("select * from JobApplication where application_id=:1", (application_id,))
            row = cur.fetchone()
            if row is None: return None
            obj = ja.JobApplication(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            obj.set_base_salary(row[8]); obj.set_experience_bonus(row[9]); obj.set_offered_salary(row[10])
            return obj

    def find_senior_applicants(self, start_date, end_date):
        with conn.cursor() as cur:
            cur.execute("""select application_id, years_exp from JobApplication
                           where years_exp > 7 and application_date between :1 and :2""",
                        (start_date, end_date))
            return {aid: yrs for aid, yrs in cur.fetchall()}

    def update_offered_salary(self, experience_grade):
        with conn.cursor() as cur:
            cur.execute("""update JobApplication
                           set offered_salary = offered_salary * 1.10,
                               experience_bonus = experience_bonus * 1.10
                           where experience_grade = :1""", (experience_grade,))
            conn.commit()
            cur.execute("select * from JobApplication where experience_grade = :1", (experience_grade,))
            rows = cur.fetchall()
            if not rows: return None
            result = []
            for row in rows:
                obj = ja.JobApplication(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                obj.set_base_salary(row[8]); obj.set_experience_bonus(row[9]); obj.set_offered_salary(row[10])
                result.append(obj)
            return result
