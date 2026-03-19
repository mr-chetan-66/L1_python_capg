import utility as ut
import medicine as md
from datetime import timedelta
import oracledb
import med_exception as me

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])

MARGIN_RATES = {"Tablet": 0.12, "Capsule": 0.18, "Syrup": 0.10}

class MedService:

    def __init__(self):
        self.__margin_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE Medicine")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_med_code(part[1])
                ut.validate_stock_id(part[0])
                mfg = ut.convert_date(part[6])
                exp = ut.convert_date(part[7])
                obj = md.Medicine(part[0], part[1], part[2], part[3],
                                  float(part[4]), int(part[5]), mfg, exp)
                margin = obj.calculate_selling_price()
                self.add_medicine_details(obj)
                self.__margin_dict[obj.get_stock_id()] = margin
            except me.InvalidMedCodeException as e:
                print(e.get_message())
            except me.InvalidStockIdException as e:
                print(e.get_message())
        return None

    def add_medicine_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into Medicine values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
            l = [obj.get_stock_id(), obj.get_med_code(), obj.get_med_name(),
                 obj.get_category(), obj.get_unit_price(), obj.get_quantity(),
                 obj.get_manufacture_date(), obj.get_expiry_date(),
                 obj.get_margin_amount(), obj.get_selling_price(), obj.get_total_stock_value()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_medicines(self):
        with conn.cursor() as cur:
            cur.execute("select * from Medicine")
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

    def search_stock(self, stock_id):
        with conn.cursor() as cur:
            cur.execute("select * from Medicine where stock_id=:1", (stock_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = md.Medicine(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            obj.set_margin_amount(row[8])
            obj.set_selling_price(row[9])
            obj.set_total_stock_value(row[10])
            return obj

    def find_near_expiry(self, ref_date, days_threshold):
        with conn.cursor() as cur:
            end_date = ref_date + timedelta(days=days_threshold)
            q = """select stock_id, expiry_date from Medicine
                   where quantity > 100
                   and expiry_date between :1 and :2"""
            cur.execute(q, (ref_date, end_date))
            rows = cur.fetchall()
            return {sid: exp for sid, exp in rows}

    def update_unit_price(self, category):
        rate = MARGIN_RATES.get(category, 0.08)
        with conn.cursor() as cur:
            q1 = f"""update Medicine
                     set unit_price = unit_price * 1.08,
                         margin_amount = unit_price * 1.08 * {rate},
                         selling_price = unit_price * 1.08 * {1 + rate},
                         total_stock_value = unit_price * 1.08 * {1 + rate} * quantity
                     where category = :1"""
            cur.execute(q1, (category,))
            conn.commit()
            cur.execute("select * from Medicine where category = :1", (category,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = md.Medicine(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                obj.set_margin_amount(row[8])
                obj.set_selling_price(row[9])
                obj.set_total_stock_value(row[10])
                result.append(obj)
            return result
