import utility as ut
import meter_reading as mr
from datetime import timedelta
import oracledb
import power_exception as pe

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class PowerService:

    def __init__(self):
        self.__fixed_charge_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE MeterReading")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_meter_code(part[1])
                ut.validate_reading_id(part[0])
                rd = ut.convert_date(part[5])
                bd = ut.convert_date(part[6])
                obj = mr.MeterReading(part[0], part[1], part[2], part[3],
                                      int(part[4]), rd, bd)
                fc = obj.calculate_bill()
                self.add_reading_details(obj)
                self.__fixed_charge_dict[obj.get_reading_id()] = fc
            except pe.InvalidMeterCodeException as e:
                print(e.get_message())
            except pe.InvalidReadingIdException as e:
                print(e.get_message())
        return None

    def add_reading_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into MeterReading values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)'
            l = [obj.get_reading_id(), obj.get_meter_code(), obj.get_consumer_name(),
                 obj.get_consumer_type(), obj.get_units_consumed(), obj.get_reading_date(),
                 obj.get_billing_date(), obj.get_energy_charge(), obj.get_fixed_charge(),
                 obj.get_total_bill()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_meters(self):
        with conn.cursor() as cur:
            cur.execute("select * from MeterReading")
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

    def search_reading(self, reading_id):
        with conn.cursor() as cur:
            cur.execute("select * from MeterReading where reading_id=:1", (reading_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = mr.MeterReading(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.set_energy_charge(row[7])
            obj.set_fixed_charge(row[8])
            obj.set_total_bill(row[9])
            return obj

    def find_high_consumption(self, start_date, end_date):
        with conn.cursor() as cur:
            q = """select reading_id, units_consumed from MeterReading
                   where units_consumed > 300
                   and reading_date between :1 and :2"""
            cur.execute(q, (start_date, end_date))
            rows = cur.fetchall()
            return {rid: units for rid, units in rows}

    def update_fixed_charge(self, consumer_type):
        with conn.cursor() as cur:
            q1 = """update MeterReading
                    set fixed_charge = fixed_charge * 1.10,
                        total_bill = energy_charge + (fixed_charge * 1.10)
                    where consumer_type = :1"""
            cur.execute(q1, (consumer_type,))
            conn.commit()
            cur.execute("select * from MeterReading where consumer_type = :1", (consumer_type,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = mr.MeterReading(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                obj.set_energy_charge(row[7])
                obj.set_fixed_charge(row[8])
                obj.set_total_bill(row[9])
                result.append(obj)
            return result
