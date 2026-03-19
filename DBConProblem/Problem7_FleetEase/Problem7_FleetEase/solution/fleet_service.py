import utility as ut
import vehicle_service as vs
import oracledb
import fleet_exception as fe

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])

class FleetService:
    def __init__(self):
        self.__labour_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE VehicleService")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_vehicle_id(part[1])
                ut.validate_service_id(part[0])
                sd = ut.convert_date(part[5])
                bd = ut.convert_date(part[6])
                obj = vs.VehicleService(part[0], part[1], part[2], part[3], int(part[4]), sd, bd)
                lc = obj.calculate_service_cost()
                self.add_service_details(obj)
                self.__labour_dict[obj.get_service_id()] = lc
            except fe.InvalidVehicleIdException as e: print(e.get_message())
            except fe.InvalidServiceIdException as e: print(e.get_message())
        return None

    def add_service_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into VehicleService values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)'
            cur.execute(q, [obj.get_service_id(), obj.get_vehicle_id(), obj.get_vehicle_name(),
                            obj.get_vehicle_type(), obj.get_odometer_km(), obj.get_service_date(),
                            obj.get_booking_date(), obj.get_parts_cost(), obj.get_labour_cost(), obj.get_total_cost()])
            conn.commit()
        return None

    def find_top3_vehicles(self):
        with conn.cursor() as cur:
            cur.execute("select * from VehicleService")
            freq = {}
            for row in cur.fetchall():
                freq[row[1]] = freq.get(row[1], 0) + 1
            sorted_f = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}; i = prev = 0
            for k, v in sorted_f.items():
                if v != prev: prev = v; i += 1
                if i > 3: break
                res[k] = v
            return res

    def search_service(self, service_id):
        with conn.cursor() as cur:
            cur.execute("select * from VehicleService where service_id=:1", (service_id,))
            row = cur.fetchone()
            if row is None: return None
            obj = vs.VehicleService(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.set_parts_cost(row[7]); obj.set_labour_cost(row[8]); obj.set_total_cost(row[9])
            return obj

    def find_high_mileage(self, start_date, end_date):
        with conn.cursor() as cur:
            cur.execute("""select service_id, odometer_km from VehicleService
                           where odometer_km > 60000 and service_date between :1 and :2""",
                        (start_date, end_date))
            return {sid: km for sid, km in cur.fetchall()}

    def update_labour_cost(self, vehicle_type):
        with conn.cursor() as cur:
            cur.execute("""update VehicleService set labour_cost = labour_cost * 1.08,
                           total_cost = parts_cost + (labour_cost * 1.08)
                           where vehicle_type = :1""", (vehicle_type,))
            conn.commit()
            cur.execute("select * from VehicleService where vehicle_type = :1", (vehicle_type,))
            rows = cur.fetchall()
            if not rows: return None
            result = []
            for row in rows:
                obj = vs.VehicleService(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                obj.set_parts_cost(row[7]); obj.set_labour_cost(row[8]); obj.set_total_cost(row[9])
                result.append(obj)
            return result
