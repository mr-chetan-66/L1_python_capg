import oracledb
import utility as ut
import exception as ex
import patient_billing as pb

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class PatientBillingService:

    def __init__(self):
        self.__patient_billing_list = []

    def get_patient_billing_details(self, input_file):
        records = ut.read_file(input_file)
        self.build_patient_billing_list(records)
        return self.__patient_billing_list

    def build_patient_billing_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_bill_id(row[0])
                ut.validate_ward_type(row[3])
                doa = ut.convert_date(row[2])
                dod = ut.convert_date(row[4])

                obj = pb.PatientBilling(row[0], row[1], doa, row[3], dod,
                                        int(row[5]), row[6], row[7])

                costs = self.calculate_billing_costs(int(row[5]), row[3])
                obj.set_bed_charges(costs[0])
                obj.set_treatment_charges(costs[1])
                obj.set_nursing_charges(costs[2])
                obj.set_discount(costs[3])
                obj.set_total_bill_amount(costs[4])

                self.__patient_billing_list.append(obj)

            except ex.InvalidBillIdException as e:
                print(e.get_message())
            except ex.InvalidWardTypeException as e:
                print(e.get_message())

        return None

    def calculate_billing_costs(self, no_of_days, ward_type):
        if ward_type == 'General':
            bpd, tpd, npd, disc_pct = 500.0, 800.0, 300.0, 5.0
        elif ward_type == 'Semi-Private':
            bpd, tpd, npd, disc_pct = 1500.0, 1500.0, 600.0, 3.0
        elif ward_type == 'Private':
            bpd, tpd, npd, disc_pct = 3000.0, 2500.0, 1000.0, 2.0
        elif ward_type == 'ICU':
            bpd, tpd, npd, disc_pct = 8000.0, 5000.0, 2000.0, 0.0

        bed = bpd * no_of_days
        treatment = tpd * no_of_days
        nursing = npd * no_of_days
        gross = bed + treatment + nursing
        discount = gross * disc_pct / 100
        total = gross - discount

        return [bed, treatment, nursing, discount, total]

    def add_billing_details(self, billing_list):
        with conn.cursor() as cur:
            for obj in billing_list:
                q = """insert into patient_billing values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                l = [obj.get_bill_id(), obj.get_patient_id(), obj.get_date_of_admission(),
                     obj.get_ward_type(), obj.get_date_of_discharge(), obj.get_no_of_days(),
                     obj.get_treatment_code(), obj.get_insurance_status(),
                     obj.get_bed_charges(), obj.get_treatment_charges(),
                     obj.get_nursing_charges(), obj.get_discount(), obj.get_total_bill_amount()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_billing_record(self, bill_id):
        with conn.cursor() as cur:
            q = """select * from patient_billing where bill_id=:1"""
            cur.execute(q, (bill_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = pb.PatientBilling(row[0], row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7])
            obj.set_bed_charges(row[8])
            obj.set_treatment_charges(row[9])
            obj.set_nursing_charges(row[10])
            obj.set_discount(row[11])
            obj.set_total_bill_amount(row[12])
            return obj

    def update_charges(self, no_days):
        with conn.cursor() as cur:
            # Increase bed and nursing by 15%, recalculate total
            # In Oracle, RHS expressions all reference the ORIGINAL column values,
            # so bed_charges * 1.15 in the total expression correctly gives the new value.
            q1 = """update patient_billing
                    set bed_charges = bed_charges * 1.15,
                        nursing_charges = nursing_charges * 1.15,
                        total_bill_amount = bed_charges * 1.15 + treatment_charges
                                           + nursing_charges * 1.15 - discount
                    where no_of_days > :1"""
            cur.execute(q1, (no_days,))
            conn.commit()

            q2 = """select * from patient_billing where no_of_days > :1"""
            cur.execute(q2, (no_days,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = pb.PatientBilling(obj[0], obj[1], obj[2], obj[3], obj[4],
                                         obj[5], obj[6], obj[7])
                sobj.set_bed_charges(obj[8])
                sobj.set_treatment_charges(obj[9])
                sobj.set_nursing_charges(obj[10])
                sobj.set_discount(obj[11])
                sobj.set_total_bill_amount(obj[12])
                ans.append(sobj)
            return ans
