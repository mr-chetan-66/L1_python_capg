import oracledb
import utility as ut
import exception as ex
import equipment_maintenance as em

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class MaintenanceService:

    def __init__(self):
        self.__maintenance_list = []

    def get_maintenance_details(self, input_file):
        records = ut.read_file(input_file)
        self.build_maintenance_list(records)
        return self.__maintenance_list

    def build_maintenance_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_maintenance_id(row[0])
                ut.validate_equipment_type(row[3])

                dls = ut.convert_date(row[2])
                dns = ut.convert_date(row[4])

                obj = em.EquipmentMaintenance(row[0], row[1], dls, row[3],
                                              dns, int(row[5]), row[6], row[7])

                costs = self.calculate_maintenance_costs(row[3], int(row[5]), row[6])
                obj.set_base_service_cost(costs[0])
                obj.set_parts_cost(costs[1])
                obj.set_technician_fee(costs[2])
                obj.set_overhaul_surcharge(costs[3])
                obj.set_total_maintenance_cost(costs[4])

                self.__maintenance_list.append(obj)

            except ex.InvalidMaintenanceIdException as e:
                print(e.get_message())
            except ex.InvalidEquipmentTypeException as e:
                print(e.get_message())

        return None

    def calculate_maintenance_costs(self, equipment_type, operating_hours, technician_grade):
        # Step 1: Base service cost
        base_map = {'CNC': 15000.0, 'Hydraulic': 12000.0,
                    'Conveyor': 8000.0, 'Electrical': 6000.0}
        base_service_cost = base_map[equipment_type]

        # Step 2: Parts cost by operating hours tier
        if operating_hours < 500:
            parts_cost = 2000.0
        elif operating_hours < 1500:
            parts_cost = 5000.0
        elif operating_hours < 2500:
            parts_cost = 10000.0
        else:
            parts_cost = 18000.0

        # Step 3: Technician fee
        grade_map = {'Grade_A': 8000.0, 'Grade_B': 5000.0, 'Grade_C': 2500.0}
        technician_fee = grade_map[technician_grade]

        # Step 4: Overhaul surcharge if operating_hours > 2000
        if operating_hours > 2000:
            overhaul_surcharge = (base_service_cost + parts_cost) * 0.20
        else:
            overhaul_surcharge = 0.0

        # Step 5: Total
        total_maintenance_cost = (base_service_cost + parts_cost
                                  + technician_fee + overhaul_surcharge)

        return [base_service_cost, parts_cost, technician_fee,
                overhaul_surcharge, total_maintenance_cost]

    def add_maintenance_details(self, maintenance_list):
        with conn.cursor() as cur:
            for obj in maintenance_list:
                q = """insert into equipment_maintenance values
                       (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                l = [obj.get_maintenance_id(), obj.get_equipment_id(),
                     obj.get_date_of_last_service(), obj.get_equipment_type(),
                     obj.get_date_of_next_service(), obj.get_operating_hours(),
                     obj.get_technician_grade(), obj.get_maintenance_status(),
                     obj.get_base_service_cost(), obj.get_parts_cost(),
                     obj.get_technician_fee(), obj.get_overhaul_surcharge(),
                     obj.get_total_maintenance_cost()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_maintenance_record(self, maintenance_id):
        with conn.cursor() as cur:
            q = """select * from equipment_maintenance where maintenance_id=:1"""
            cur.execute(q, (maintenance_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = em.EquipmentMaintenance(row[0], row[1], row[2], row[3],
                                          row[4], row[5], row[6], row[7])
            obj.set_base_service_cost(row[8])
            obj.set_parts_cost(row[9])
            obj.set_technician_fee(row[10])
            obj.set_overhaul_surcharge(row[11])
            obj.set_total_maintenance_cost(row[12])
            return obj

    def update_parts_cost(self, operating_hours_threshold):
        with conn.cursor() as cur:
            q1 = """update equipment_maintenance
                    set parts_cost             = parts_cost * 1.08,
                        total_maintenance_cost = base_service_cost
                                                 + parts_cost * 1.08
                                                 + technician_fee
                                                 + overhaul_surcharge
                    where operating_hours > :1"""
            cur.execute(q1, (operating_hours_threshold,))
            conn.commit()

            q2 = """select * from equipment_maintenance where operating_hours > :1"""
            cur.execute(q2, (operating_hours_threshold,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = em.EquipmentMaintenance(obj[0], obj[1], obj[2], obj[3],
                                               obj[4], obj[5], obj[6], obj[7])
                sobj.set_base_service_cost(obj[8])
                sobj.set_parts_cost(obj[9])
                sobj.set_technician_fee(obj[10])
                sobj.set_overhaul_surcharge(obj[11])
                sobj.set_total_maintenance_cost(obj[12])
                ans.append(sobj)
            return ans
