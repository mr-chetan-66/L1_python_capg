### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE

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
        """
        Call utility.read_file() with input_file.
        Pass the result to build_maintenance_list().
        Return __maintenance_list.
        """
        # Write your code here
        pass

    def build_maintenance_list(self, records):
        """
        For each record string:
          1. Validate maintenance_id  -> catch InvalidMaintenanceIdException, print message
          2. Validate equipment_type  -> catch InvalidEquipmentTypeException, print message
          3. Convert date strings using utility.convert_date()
          4. Create an EquipmentMaintenance object
          5. Call calculate_maintenance_costs() and set all cost attributes
          6. Append the object to __maintenance_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_maintenance_costs(self, equipment_type, operating_hours, technician_grade):
        """
        Return [base_service_cost, parts_cost, technician_fee,
                overhaul_surcharge, total_maintenance_cost] as a list of floats.

        Step 1 – Base service cost by equipment_type (INR, flat per service):
        +------------+--------------------+
        | Type       | Base Service Cost  |
        +------------+--------------------+
        | CNC        |     15,000         |
        | Hydraulic  |     12,000         |
        | Conveyor   |      8,000         |
        | Electrical |      6,000         |
        +------------+--------------------+

        Step 2 – Parts cost by operating_hours tier (INR, flat):
        +---------------------+------------+
        | Operating Hours     | Parts Cost |
        +---------------------+------------+
        | Below 500           |   2,000    |
        | 500  – 1,499        |   5,000    |
        | 1,500 – 2,499       |  10,000    |
        | 2,500 and above     |  18,000    |
        +---------------------+------------+

        Step 3 – Technician fee by technician_grade (INR, flat per service):
        +-----------+----------------+
        | Grade     | Technician Fee |
        +-----------+----------------+
        | Grade_A   |    8,000       |
        | Grade_B   |    5,000       |
        | Grade_C   |    2,500       |
        +-----------+----------------+

        Step 4 – Overhaul surcharge:
        If operating_hours > 2000:
            overhaul_surcharge = (base_service_cost + parts_cost) * 0.20
        Else:
            overhaul_surcharge = 0.0

        Step 5:
        total_maintenance_cost = base_service_cost + parts_cost
                                 + technician_fee + overhaul_surcharge
        """
        # Write your code here
        pass

    def add_maintenance_details(self, maintenance_list):
        """
        Insert each EquipmentMaintenance object into 'equipment_maintenance' table.
        Column order: maintenance_id, equipment_id, date_of_last_service,
                      equipment_type, date_of_next_service, operating_hours,
                      technician_grade, maintenance_status, base_service_cost,
                      parts_cost, technician_fee, overhaul_surcharge,
                      total_maintenance_cost
        Returns None.
        """
        # Write your code here
        pass

    def search_maintenance_record(self, maintenance_id):
        """
        Query 'equipment_maintenance' by maintenance_id.
        If found, return a fully populated EquipmentMaintenance object.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_parts_cost(self, operating_hours_threshold):
        """
        For all records where operating_hours > operating_hours_threshold:
          - Increase parts_cost by 8%
          - Recalculate total_maintenance_cost =
              base_service_cost + new_parts_cost + technician_fee + overhaul_surcharge
        Commit the update.
        Fetch and return all updated EquipmentMaintenance objects as a list.
        Return None if no records qualify.
        """
        # Write your code here
        pass
