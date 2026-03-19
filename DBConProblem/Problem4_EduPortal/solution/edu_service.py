import utility as ut
import enrollment as en
from datetime import timedelta
import oracledb
import edu_exception as ee

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class EduService:

    def __init__(self):
        self.__scholarship_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE Enrollment")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_course_code(part[1])
                ut.validate_enrollment_id(part[0])
                start = ut.convert_date(part[5])
                reg = ut.convert_date(part[6])
                obj = en.Enrollment(part[0], part[1], part[2], part[3],
                                    int(part[4]), start, reg, part[7])
                scholarship = obj.calculate_fee()
                self.add_enrollment_details(obj)
                self.__scholarship_dict[obj.get_enrollment_id()] = scholarship
            except ee.InvalidCourseCodeException as e:
                print(e.get_message())
            except ee.InvalidEnrollmentIdException as e:
                print(e.get_message())
        return None

    def add_enrollment_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into Enrollment values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
            l = [obj.get_enrollment_id(), obj.get_course_code(), obj.get_student_name(),
                 obj.get_grade_level(), obj.get_duration_days(), obj.get_start_date(),
                 obj.get_registration_date(), obj.get_course_name(),
                 obj.get_base_fee(), obj.get_scholarship_amount(), obj.get_payable_fee()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_courses(self):
        with conn.cursor() as cur:
            cur.execute("select * from Enrollment")
            rows = cur.fetchall()
            freq = {}
            for row in rows:
                code = row[1]
                freq[code] = freq.get(code, 0) + 1
            sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}
            i, prev = 0, 0
            for k, v in sorted_freq.items():
                if v != prev:
                    prev = v
                    i += 1
                if i > 3:
                    break
                res[k] = v
            return res

    def search_enrollment(self, enrollment_id):
        with conn.cursor() as cur:
            cur.execute("select * from Enrollment where enrollment_id=:1", (enrollment_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = en.Enrollment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            obj.set_base_fee(row[8])
            obj.set_scholarship_amount(row[9])
            obj.set_payable_fee(row[10])
            return obj

    def find_completion_dates(self, start_date, end_date):
        with conn.cursor() as cur:
            q = """select enrollment_id, start_date, duration_days from Enrollment
                   where duration_days > 35
                   and start_date between :1 and :2"""
            cur.execute(q, (start_date, end_date))
            rows = cur.fetchall()
            return {eid: (d + timedelta(days=nd)) for eid, d, nd in rows}

    def update_payable_fee(self, grade_level):
        with conn.cursor() as cur:
            q1 = """update Enrollment
                    set scholarship_amount = scholarship_amount * 1.15,
                        payable_fee = base_fee - (scholarship_amount * 1.15)
                    where grade_level = :1"""
            cur.execute(q1, (grade_level,))
            conn.commit()
            cur.execute("select * from Enrollment where grade_level = :1", (grade_level,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = en.Enrollment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                obj.set_base_fee(row[8])
                obj.set_scholarship_amount(row[9])
                obj.set_payable_fee(row[10])
                result.append(obj)
            return result
