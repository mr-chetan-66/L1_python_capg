# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class EquipmentMaintenance:

    # Define the parameterized constructor here
    # Parameters: maintenance_id, equipment_id, date_of_last_service,
    #             equipment_type, date_of_next_service, operating_hours,
    #             technician_grade, maintenance_status
    # Default values: base_service_cost=0.0, parts_cost=0.0,
    #                 technician_fee=0.0, overhaul_surcharge=0.0,
    #                 total_maintenance_cost=0.0
    def __init__(self, maintenance_id: str, equipment_id: str,
                 date_of_last_service: date, equipment_type: str,
                 date_of_next_service: date, operating_hours: int,
                 technician_grade: str, maintenance_status: str):
        # Write your code here
        pass

    # Write all getters and setters for the private attributes below

    def get_maintenance_id(self):
        pass
    def set_maintenance_id(self, maintenance_id):
        pass

    def get_equipment_id(self):
        pass
    def set_equipment_id(self, equipment_id):
        pass

    def get_date_of_last_service(self):
        pass
    def set_date_of_last_service(self, date_of_last_service):
        pass

    def get_equipment_type(self):
        pass
    def set_equipment_type(self, equipment_type):
        pass

    def get_date_of_next_service(self):
        pass
    def set_date_of_next_service(self, date_of_next_service):
        pass

    def get_operating_hours(self):
        pass
    def set_operating_hours(self, operating_hours):
        pass

    def get_technician_grade(self):
        pass
    def set_technician_grade(self, technician_grade):
        pass

    def get_maintenance_status(self):
        pass
    def set_maintenance_status(self, maintenance_status):
        pass

    def get_base_service_cost(self):
        pass
    def set_base_service_cost(self, base_service_cost):
        pass

    def get_parts_cost(self):
        pass
    def set_parts_cost(self, parts_cost):
        pass

    def get_technician_fee(self):
        pass
    def set_technician_fee(self, technician_fee):
        pass

    def get_overhaul_surcharge(self):
        pass
    def set_overhaul_surcharge(self, overhaul_surcharge):
        pass

    def get_total_maintenance_cost(self):
        pass
    def set_total_maintenance_cost(self, total_maintenance_cost):
        pass
