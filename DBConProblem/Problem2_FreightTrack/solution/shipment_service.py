import utility as ut
import shipment as sh
from datetime import timedelta
import oracledb
import freight_exception as fe

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class ShipmentService:

    def __init__(self):
        self.__surcharge_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE Shipment")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_freight_id(part[1])
                ut.validate_shipment_id(part[0])
                d = ut.convert_date(part[5])
                obj = sh.Shipment(part[0], part[1], part[2],
                                  float(part[3]), int(part[4]), d, part[6])
                sur = obj.calculate_base_charge()
                self.add_shipment_details(obj)
                if sur > 0:
                    self.__surcharge_dict[obj.get_shipment_id()] = sur
            except fe.InvalidFreightIdException as e:
                print(e.get_message())
            except fe.InvalidShipmentIdException as e:
                print(e.get_message())
        return None

    def add_shipment_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into Shipment values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)'
            l = [obj.get_shipment_id(), obj.get_freight_id(), obj.get_client_name(),
                 obj.get_weight_kg(), obj.get_no_of_days(), obj.get_dispatch_date(),
                 obj.get_service_type(), obj.get_base_charge(), obj.get_surcharge(),
                 obj.get_total_charge()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_freight(self):
        with conn.cursor() as cur:
            cur.execute("select * from Shipment")
            rows = cur.fetchall()
            freq = {}
            for row in rows:
                fid = row[1]
                freq[fid] = freq.get(fid, 0) + 1
            sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}
            i = 0
            prev = 0
            for k, v in sorted_freq.items():
                if v != prev:
                    prev = v
                    i += 1
                if i > 3:
                    break
                res[k] = v
            return res

    def search_shipment(self, shipment_id):
        with conn.cursor() as cur:
            cur.execute("select * from Shipment where shipment_id=:1", (shipment_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = sh.Shipment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.set_base_charge(row[7])
            obj.set_surcharge(row[8])
            obj.set_total_charge(row[9])
            return obj

    def find_delivery_dates(self, start_date, end_date):
        with conn.cursor() as cur:
            q = """select shipment_id, dispatch_date, no_of_days from Shipment
                   where no_of_days > 4
                   and dispatch_date between :1 and :2"""
            cur.execute(q, (start_date, end_date))
            rows = cur.fetchall()
            return {sid: (d + timedelta(days=nd)) for sid, d, nd in rows}

    def update_surcharge(self, service_type):
        with conn.cursor() as cur:
            q1 = """update Shipment
                    set surcharge = surcharge * 1.12,
                        total_charge = base_charge + (surcharge * 1.12)
                    where service_type = :1"""
            cur.execute(q1, (service_type,))
            conn.commit()
            cur.execute("select * from Shipment where service_type = :1", (service_type,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = sh.Shipment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                obj.set_base_charge(row[7])
                obj.set_surcharge(row[8])
                obj.set_total_charge(row[9])
                result.append(obj)
            return result
