import oracledb
import utility as ut
import exception as ex
import shipment_order as so

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class ShipmentService:

    def __init__(self):
        self.__shipment_list = []

    def get_shipment_details(self, input_file):
        records = ut.read_file(input_file)
        self.build_shipment_list(records)
        return self.__shipment_list

    def build_shipment_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_shipment_id(row[0])
                ut.validate_zone(row[3])

                dod = ut.convert_date(row[2])
                dodl = ut.convert_date(row[4])

                obj = so.ShipmentOrder(row[0], row[1], dod, row[3], dodl,
                                       float(row[5]), row[6], row[7])

                costs = self.calculate_shipping_costs(float(row[5]), row[3], dod, dodl)
                obj.set_freight_charge(costs[0])
                obj.set_handling_charge(costs[1])
                obj.set_delay_penalty(costs[2])
                obj.set_tax(costs[3])
                obj.set_total_shipping_cost(costs[4])

                self.__shipment_list.append(obj)

            except ex.InvalidShipmentIdException as e:
                print(e.get_message())
            except ex.InvalidZoneException as e:
                print(e.get_message())

        return None

    def calculate_shipping_costs(self, weight_in_kg, zone, date_of_dispatch, date_of_delivery):
        if zone == 'Zone_A':
            fpk, hpk, tax_pct = 50.0, 10.0, 5.0
        elif zone == 'Zone_B':
            fpk, hpk, tax_pct = 80.0, 15.0, 8.0
        elif zone == 'Zone_C':
            fpk, hpk, tax_pct = 120.0, 20.0, 10.0
        elif zone == 'Zone_D':
            fpk, hpk, tax_pct = 200.0, 30.0, 12.0

        freight_charge = fpk * weight_in_kg
        handling_charge = hpk * weight_in_kg
        gross = freight_charge + handling_charge
        tax = gross * tax_pct / 100

        transit_days = (date_of_delivery - date_of_dispatch).days
        delay_penalty = weight_in_kg * 25.0 if transit_days > 7 else 0.0

        total_shipping_cost = gross + tax + delay_penalty

        return [freight_charge, handling_charge, delay_penalty, tax, total_shipping_cost]

    def add_shipment_details(self, shipment_list):
        with conn.cursor() as cur:
            for obj in shipment_list:
                q = """insert into shipment_order values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                l = [obj.get_shipment_id(), obj.get_sender_id(), obj.get_date_of_dispatch(),
                     obj.get_zone(), obj.get_date_of_delivery(), obj.get_weight_in_kg(),
                     obj.get_shipment_type(), obj.get_delivery_status(),
                     obj.get_freight_charge(), obj.get_handling_charge(),
                     obj.get_delay_penalty(), obj.get_tax(), obj.get_total_shipping_cost()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_shipment(self, shipment_id):
        with conn.cursor() as cur:
            q = """select * from shipment_order where shipment_id=:1"""
            cur.execute(q, (shipment_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = so.ShipmentOrder(row[0], row[1], row[2], row[3], row[4],
                                   row[5], row[6], row[7])
            obj.set_freight_charge(row[8])
            obj.set_handling_charge(row[9])
            obj.set_delay_penalty(row[10])
            obj.set_tax(row[11])
            obj.set_total_shipping_cost(row[12])
            return obj

    def update_freight(self, weight_threshold):
        with conn.cursor() as cur:
            q1 = """update shipment_order
                    set freight_charge = freight_charge * 1.20,
                        total_shipping_cost = freight_charge * 1.20 + handling_charge
                                              + tax + delay_penalty
                    where weight_in_kg > :1"""
            cur.execute(q1, (weight_threshold,))
            conn.commit()

            q2 = """select * from shipment_order where weight_in_kg > :1"""
            cur.execute(q2, (weight_threshold,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = so.ShipmentOrder(obj[0], obj[1], obj[2], obj[3], obj[4],
                                        obj[5], obj[6], obj[7])
                sobj.set_freight_charge(obj[8])
                sobj.set_handling_charge(obj[9])
                sobj.set_delay_penalty(obj[10])
                sobj.set_tax(obj[11])
                sobj.set_total_shipping_cost(obj[12])
                ans.append(sobj)
            return ans
