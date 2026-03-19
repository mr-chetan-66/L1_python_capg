import utility as ut
import insurance_claim as ic
import oracledb
import health_exception as he

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])

POLICY_RATES = {"Platinum": (0.95, 0.05), "Gold": (0.80, 0.20), "Silver": (0.60, 0.40), "Bronze": (0.40, 0.60)}

class HealthService:
    def __init__(self):
        self.__deductible_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE InsuranceClaim")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_policy_id(part[1])
                ut.validate_claim_id(part[0])
                cd = ut.convert_date(part[5]); pd = ut.convert_date(part[6])
                obj = ic.InsuranceClaim(part[0], part[1], part[2], part[3], float(part[4]), cd, pd)
                ded = obj.calculate_approved_amount()
                self.add_claim_details(obj)
                self.__deductible_dict[obj.get_claim_id()] = ded
            except he.InvalidPolicyIdException as e: print(e.get_message())
            except he.InvalidClaimIdException as e: print(e.get_message())
        return None

    def add_claim_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into InsuranceClaim values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)'
            cur.execute(q, [obj.get_claim_id(), obj.get_policy_id(), obj.get_patient_name(),
                            obj.get_policy_type(), obj.get_claim_amount(), obj.get_claim_date(),
                            obj.get_policy_date(), obj.get_coverage_amount(),
                            obj.get_deductible(), obj.get_approved_amount()])
            conn.commit()
        return None

    def find_top3_policies(self):
        with conn.cursor() as cur:
            cur.execute("select * from InsuranceClaim")
            freq = {}
            for row in cur.fetchall(): freq[row[1]] = freq.get(row[1], 0) + 1
            sorted_f = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}; i = prev = 0
            for k, v in sorted_f.items():
                if v != prev: prev = v; i += 1
                if i > 3: break
                res[k] = v
            return res

    def search_claim(self, claim_id):
        with conn.cursor() as cur:
            cur.execute("select * from InsuranceClaim where claim_id=:1", (claim_id,))
            row = cur.fetchone()
            if row is None: return None
            obj = ic.InsuranceClaim(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.set_coverage_amount(row[7]); obj.set_deductible(row[8]); obj.set_approved_amount(row[9])
            return obj

    def find_high_value_claims(self, start_date, end_date):
        with conn.cursor() as cur:
            cur.execute("""select claim_id, claim_amount from InsuranceClaim
                           where claim_amount > 100000 and claim_date between :1 and :2""",
                        (start_date, end_date))
            return {cid: amt for cid, amt in cur.fetchall()}

    def update_approved_amount(self, policy_type):
        with conn.cursor() as cur:
            cur.execute("""update InsuranceClaim
                           set approved_amount = approved_amount * 1.05,
                               coverage_amount = approved_amount * 1.05
                           where policy_type = :1""", (policy_type,))
            conn.commit()
            cur.execute("select * from InsuranceClaim where policy_type = :1", (policy_type,))
            rows = cur.fetchall()
            if not rows: return None
            result = []
            for row in rows:
                obj = ic.InsuranceClaim(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                obj.set_coverage_amount(row[7]); obj.set_deductible(row[8]); obj.set_approved_amount(row[9])
                result.append(obj)
            return result
