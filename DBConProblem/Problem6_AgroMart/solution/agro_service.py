import utility as ut
import crop as cr
from datetime import timedelta
import oracledb
import agro_exception as ae

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])

SEASON_RATES = {"Kharif": 0.15, "Rabi": 0.10, "Summer": 0.05}

class AgroService:

    def __init__(self):
        self.__premium_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE Crop")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_crop_code(part[1])
                ut.validate_agri_id(part[0])
                hd = ut.convert_date(part[7])
                ld = ut.convert_date(part[8])
                obj = cr.Crop(part[0], part[1], part[2], part[3],
                              float(part[4]), int(part[5]), part[6], hd, ld)
                premium = obj.calculate_selling_price()
                self.add_crop_details(obj)
                self.__premium_dict[obj.get_agri_id()] = premium
            except ae.InvalidCropCodeException as e:
                print(e.get_message())
            except ae.InvalidAgriIdException as e:
                print(e.get_message())
        return None

    def add_crop_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into Crop values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)'
            l = [obj.get_agri_id(), obj.get_crop_code(), obj.get_crop_name(),
                 obj.get_crop_type(), obj.get_base_price(), obj.get_quantity_kg(),
                 obj.get_season(), obj.get_harvest_date(), obj.get_listing_date(),
                 obj.get_seasonal_premium(), obj.get_selling_price(), obj.get_total_value()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_crops(self):
        with conn.cursor() as cur:
            cur.execute("select * from Crop")
            rows = cur.fetchall()
            freq = {}
            for row in rows:
                freq[row[1]] = freq.get(row[1], 0) + 1
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

    def search_crop(self, agri_id):
        with conn.cursor() as cur:
            cur.execute("select * from Crop where agri_id=:1", (agri_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = cr.Crop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            obj.set_seasonal_premium(row[9])
            obj.set_selling_price(row[10])
            obj.set_total_value(row[11])
            return obj

    def find_bulk_stock(self, start_date, end_date):
        with conn.cursor() as cur:
            q = """select agri_id, quantity_kg from Crop
                   where quantity_kg > 4000
                   and harvest_date between :1 and :2"""
            cur.execute(q, (start_date, end_date))
            rows = cur.fetchall()
            return {aid: qty for aid, qty in rows}

    def update_base_price(self, season):
        rate = SEASON_RATES.get(season, 0.0)
        sp_factor = 1 + rate
        with conn.cursor() as cur:
            q1 = f"""update Crop
                     set base_price = base_price * 1.12,
                         seasonal_premium = base_price * 1.12 * {rate},
                         selling_price = base_price * 1.12 * {sp_factor},
                         total_value = base_price * 1.12 * {sp_factor} * quantity_kg
                     where season = :1"""
            cur.execute(q1, (season,))
            conn.commit()
            cur.execute("select * from Crop where season = :1", (season,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = cr.Crop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                obj.set_seasonal_premium(row[9])
                obj.set_selling_price(row[10])
                obj.set_total_value(row[11])
                result.append(obj)
            return result
