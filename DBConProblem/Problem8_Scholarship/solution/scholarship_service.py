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
        records = ut.read_file(input_file)
        self.build_scholarship_list(records)
        return self.__scholarship_list

    def build_scholarship_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_application_id(row[0])
                ut.validate_course_type(row[3])

                doa = ut.convert_date(row[2])
                doe = ut.convert_date(row[4])

                obj = sa.ScholarshipApplication(
                    row[0], row[1], doa, row[3], doe,
                    float(row[5]), float(row[6]), row[7], row[8]
                )

                costs = self.calculate_scholarship(row[3], float(row[5]),
                                                   float(row[6]), row[7])
                obj.set_base_scholarship(costs[0])
                obj.set_merit_bonus(costs[1])
                obj.set_income_waiver(costs[2])
                obj.set_total_scholarship(costs[3])

                self.__scholarship_list.append(obj)

            except ex.InvalidApplicationIdException as e:
                print(e.get_message())
            except ex.InvalidCourseTypeException as e:
                print(e.get_message())

        return None

    def calculate_scholarship(self, course_type, cgpa, annual_family_income, category):
        # Step 1: Base scholarship by course type
        base_map = {'UG': 40000.0, 'PG': 60000.0, 'Diploma': 25000.0, 'PhD': 100000.0}
        base_scholarship = base_map[course_type]

        # Step 2: Merit bonus % by CGPA
        if cgpa >= 9.0:
            merit_pct = 25.0
        elif cgpa >= 8.0:
            merit_pct = 15.0
        elif cgpa >= 7.0:
            merit_pct = 8.0
        else:
            merit_pct = 0.0
        merit_bonus = base_scholarship * merit_pct / 100

        # Step 3: Income waiver flat amount
        if annual_family_income < 100000:
            income_waiver = 15000.0
        elif annual_family_income < 250000:
            income_waiver = 8000.0
        elif annual_family_income < 500000:
            income_waiver = 3000.0
        else:
            income_waiver = 0.0

        # Step 4: Category multiplier on total
        multiplier_map = {'SC': 1.20, 'ST': 1.25, 'OBC': 1.10, 'General': 1.00}
        multiplier = multiplier_map[category]

        total_scholarship = round(
            (base_scholarship + merit_bonus + income_waiver) * multiplier, 2
        )

        return [base_scholarship, merit_bonus, income_waiver, total_scholarship]

    def add_scholarship_details(self, scholarship_list):
        with conn.cursor() as cur:
            for obj in scholarship_list:
                q = """insert into scholarship_application values
                       (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                l = [obj.get_application_id(), obj.get_student_id(),
                     obj.get_date_of_application(), obj.get_course_type(),
                     obj.get_date_of_enrollment(), obj.get_cgpa(),
                     obj.get_annual_family_income(), obj.get_category(),
                     obj.get_application_status(), obj.get_base_scholarship(),
                     obj.get_merit_bonus(), obj.get_income_waiver(),
                     obj.get_total_scholarship()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_application(self, application_id):
        with conn.cursor() as cur:
            q = """select * from scholarship_application where application_id=:1"""
            cur.execute(q, (application_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = sa.ScholarshipApplication(
                row[0], row[1], row[2], row[3], row[4],
                row[5], row[6], row[7], row[8]
            )
            obj.set_base_scholarship(row[9])
            obj.set_merit_bonus(row[10])
            obj.set_income_waiver(row[11])
            obj.set_total_scholarship(row[12])
            return obj

    def update_merit_bonus(self, cgpa_threshold):
        with conn.cursor() as cur:
            q1 = """update scholarship_application
                    set merit_bonus        = merit_bonus * 1.10,
                        total_scholarship  = base_scholarship
                                             + merit_bonus * 1.10
                                             + income_waiver
                    where cgpa > :1"""
            cur.execute(q1, (cgpa_threshold,))
            conn.commit()

            q2 = """select * from scholarship_application where cgpa > :1"""
            cur.execute(q2, (cgpa_threshold,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = sa.ScholarshipApplication(
                    obj[0], obj[1], obj[2], obj[3], obj[4],
                    obj[5], obj[6], obj[7], obj[8]
                )
                sobj.set_base_scholarship(obj[9])
                sobj.set_merit_bonus(obj[10])
                sobj.set_income_waiver(obj[11])
                sobj.set_total_scholarship(obj[12])
                ans.append(sobj)
            return ans
