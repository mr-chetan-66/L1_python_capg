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
        records = ut.read_file(input_file)
        self.build_loan_list(records)
        return self.__loan_list

    def build_loan_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_loan_id(row[0])
                ut.validate_loan_type(row[3])

                doa = ut.convert_date(row[2])
                dod = ut.convert_date(row[4])

                obj = la.LoanApplication(row[0], row[1], doa, row[3], dod,
                                         float(row[5]), int(row[6]),
                                         int(row[7]), row[8])

                costs = self.calculate_loan_costs(float(row[5]), int(row[6]),
                                                  row[3], int(row[7]))
                obj.set_annual_interest_rate(costs[0])
                obj.set_processing_fee(costs[1])
                obj.set_monthly_emi(costs[2])
                obj.set_total_interest(costs[3])
                obj.set_total_repayment(costs[4])

                self.__loan_list.append(obj)

            except ex.InvalidLoanIdException as e:
                print(e.get_message())
            except ex.InvalidLoanTypeException as e:
                print(e.get_message())

        return None

    def _compute_emi(self, loan_amount, annual_interest_rate, tenure_in_months):
        """Helper: standard reducing-balance EMI formula."""
        r = annual_interest_rate / 12 / 100
        n = tenure_in_months
        emi = loan_amount * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        return round(emi, 2)

    def calculate_loan_costs(self, loan_amount, tenure_in_months, loan_type, credit_score):
        # Step 1: Base rate by loan type
        base_rates = {'Home': 7.0, 'Vehicle': 9.0, 'Personal': 13.0, 'Education': 6.0}
        base_rate = base_rates[loan_type]

        # Step 2: Credit score adjustment
        if credit_score >= 750:
            adjustment = -1.5
        elif credit_score >= 700:
            adjustment = -0.75
        elif credit_score >= 650:
            adjustment = 0.0
        else:
            adjustment = 1.0   # surcharge

        annual_interest_rate = base_rate + adjustment

        # Step 3: Processing fee
        fee_pcts = {'Home': 0.5, 'Vehicle': 1.0, 'Personal': 2.0, 'Education': 0.25}
        processing_fee = round(loan_amount * fee_pcts[loan_type] / 100, 2)

        # Step 4: EMI
        monthly_emi = self._compute_emi(loan_amount, annual_interest_rate, tenure_in_months)

        # Step 5: Totals
        total_repayment = round(monthly_emi * tenure_in_months, 2)
        total_interest = round(total_repayment - loan_amount, 2)

        return [annual_interest_rate, processing_fee, monthly_emi,
                total_interest, total_repayment]

    def add_loan_details(self, loan_list):
        with conn.cursor() as cur:
            for obj in loan_list:
                q = """insert into loan_application values
                       (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)"""
                l = [obj.get_loan_id(), obj.get_applicant_id(),
                     obj.get_date_of_application(), obj.get_loan_type(),
                     obj.get_date_of_disbursement(), obj.get_loan_amount(),
                     obj.get_tenure_in_months(), obj.get_credit_score(),
                     obj.get_loan_status(), obj.get_annual_interest_rate(),
                     obj.get_processing_fee(), obj.get_monthly_emi(),
                     obj.get_total_interest(), obj.get_total_repayment()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_loan(self, loan_id):
        with conn.cursor() as cur:
            q = """select * from loan_application where loan_id=:1"""
            cur.execute(q, (loan_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = la.LoanApplication(row[0], row[1], row[2], row[3], row[4],
                                     row[5], row[6], row[7], row[8])
            obj.set_annual_interest_rate(row[9])
            obj.set_processing_fee(row[10])
            obj.set_monthly_emi(row[11])
            obj.set_total_interest(row[12])
            obj.set_total_repayment(row[13])
            return obj

    def update_interest_rate(self, credit_score_threshold):
        with conn.cursor() as cur:
            # Fetch affected records first so we can recompute EMI in Python
            q_fetch = """select loan_id, loan_amount, tenure_in_months,
                                annual_interest_rate, credit_score
                         from loan_application
                         where credit_score < :1"""
            cur.execute(q_fetch, (credit_score_threshold,))
            affected = cur.fetchall()

            if not affected:
                return None

            for rec in affected:
                loan_id, loan_amount, tenure, old_rate, _ = rec
                new_rate = round(float(old_rate) + 0.5, 2)
                new_emi = self._compute_emi(float(loan_amount), new_rate, int(tenure))
                new_total_repayment = round(new_emi * int(tenure), 2)
                new_total_interest = round(new_total_repayment - float(loan_amount), 2)

                q_upd = """update loan_application
                           set annual_interest_rate = :1,
                               monthly_emi = :2,
                               total_interest = :3,
                               total_repayment = :4
                           where loan_id = :5"""
                cur.execute(q_upd, (new_rate, new_emi, new_total_interest,
                                    new_total_repayment, loan_id))

            conn.commit()

            q2 = """select * from loan_application where credit_score < :1"""
            cur.execute(q2, (credit_score_threshold,))
            rows = cur.fetchall()

            ans = []
            for obj in rows:
                sobj = la.LoanApplication(obj[0], obj[1], obj[2], obj[3], obj[4],
                                          obj[5], obj[6], obj[7], obj[8])
                sobj.set_annual_interest_rate(obj[9])
                sobj.set_processing_fee(obj[10])
                sobj.set_monthly_emi(obj[11])
                sobj.set_total_interest(obj[12])
                sobj.set_total_repayment(obj[13])
                ans.append(sobj)
            return ans
