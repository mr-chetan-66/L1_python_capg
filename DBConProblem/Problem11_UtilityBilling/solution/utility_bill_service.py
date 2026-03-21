import oracledb
import utility as ut
import exception as ex
import utility_bill as ub

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class UtilityBillService:

    def __init__(self):
        self.__utility_bill_list = []

    def get_utility_bill_details(self, input_file):
        records = ut.read_file(input_file)
        self.build_utility_bill_list(records)
        return self.__utility_bill_list

    def build_utility_bill_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_bill_id(row[0])
                ut.validate_consumer_type(row[3])

                bd = ut.convert_date(row[2])
                rd = ut.convert_date(row[4])

                obj = ub.UtilityBill(row[0], row[1], bd, row[3], rd,
                                     float(row[5]), row[6], row[7])

                charges = self.calculate_bill_charges(float(row[5]), row[3], row[6])
                obj.set_energy_charge(charges[0])
                obj.set_fixed_charge(charges[1])
                obj.set_tax(charges[2])
                obj.set_total_bill_amount(charges[3])

                self.__utility_bill_list.append(obj)

            except ex.InvalidBillIdException as e:
                print(e.get_message())
            except ex.InvalidConsumerTypeException as e:
                print(e.get_message())

        return None

    def calculate_bill_charges(self, units_consumed, consumer_type, connection_type):
        # Step 1: Energy charge
        if consumer_type == 'Residential':
            # Cumulative slab calculation
            if units_consumed <= 100:
                energy_charge = units_consumed * 3.0
            elif units_consumed <= 300:
                energy_charge = (100 * 3.0) + (units_consumed - 100) * 5.0
            elif units_consumed <= 500:
                energy_charge = (100 * 3.0) + (200 * 5.0) + (units_consumed - 300) * 7.0
            else:
                energy_charge = (100 * 3.0) + (200 * 5.0) + (200 * 7.0) + (units_consumed - 500) * 9.0

        elif consumer_type == 'Commercial':
            energy_charge = units_consumed * 8.0

        elif consumer_type == 'Industrial':
            energy_charge = units_consumed * 6.0 + 2000.0

        elif consumer_type == 'Agricultural':
            energy_charge = units_consumed * 1.5

        # Step 2: Fixed charge by connection type
        fixed_map = {'Single_Phase': 100.0, 'Three_Phase': 300.0, 'HT_Connection': 1000.0}
        fixed_charge = fixed_map[connection_type]

        # Step 3: Tax — 5% on energy_charge only
        tax = energy_charge * 0.05

        # Step 4: Total
        total_bill_amount = round(energy_charge + fixed_charge + tax, 2)

        return [energy_charge, fixed_charge, tax, total_bill_amount]

    def add_utility_bill_details(self, bill_list):
        with conn.cursor() as cur:
            for obj in bill_list:
                q = """insert into utility_bill values
                       (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)"""
                l = [obj.get_bill_id(), obj.get_consumer_id(),
                     obj.get_billing_date(), obj.get_consumer_type(),
                     obj.get_reading_date(), obj.get_units_consumed(),
                     obj.get_connection_type(), obj.get_payment_status(),
                     obj.get_energy_charge(), obj.get_fixed_charge(),
                     obj.get_tax(), obj.get_total_bill_amount()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_bill(self, bill_id):
        with conn.cursor() as cur:
            q = """select * from utility_bill where bill_id=:1"""
            cur.execute(q, (bill_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = ub.UtilityBill(row[0], row[1], row[2], row[3],
                                  row[4], row[5], row[6], row[7])
            obj.set_energy_charge(row[8])
            obj.set_fixed_charge(row[9])
            obj.set_tax(row[10])
            obj.set_total_bill_amount(row[11])
            return obj

    def update_energy_charges(self, units_threshold):
        with conn.cursor() as cur:
            q1 = """update utility_bill
                    set energy_charge     = energy_charge * 1.05,
                        tax               = energy_charge * 1.05 * 0.05,
                        total_bill_amount = energy_charge * 1.05
                                            + fixed_charge
                                            + energy_charge * 1.05 * 0.05
                    where units_consumed > :1"""
            cur.execute(q1, (units_threshold,))
            conn.commit()

            q2 = """select * from utility_bill where units_consumed > :1"""
            cur.execute(q2, (units_threshold,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = ub.UtilityBill(obj[0], obj[1], obj[2], obj[3],
                                      obj[4], obj[5], obj[6], obj[7])
                sobj.set_energy_charge(obj[8])
                sobj.set_fixed_charge(obj[9])
                sobj.set_tax(obj[10])
                sobj.set_total_bill_amount(obj[11])
                ans.append(sobj)
            return ans
