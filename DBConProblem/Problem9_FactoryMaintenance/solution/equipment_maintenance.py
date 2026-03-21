from datetime import date

class EquipmentMaintenance:

    def __init__(self, maintenance_id: str, equipment_id: str,
                 date_of_last_service: date, equipment_type: str,
                 date_of_next_service: date, operating_hours: int,
                 technician_grade: str, maintenance_status: str):
        self.__maintenance_id = maintenance_id
        self.__equipment_id = equipment_id
        self.__date_of_last_service = date_of_last_service
        self.__equipment_type = equipment_type
        self.__date_of_next_service = date_of_next_service
        self.__operating_hours = operating_hours
        self.__technician_grade = technician_grade
        self.__maintenance_status = maintenance_status
        self.__base_service_cost = 0.0
        self.__parts_cost = 0.0
        self.__technician_fee = 0.0
        self.__overhaul_surcharge = 0.0
        self.__total_maintenance_cost = 0.0

    def get_maintenance_id(self): return self.__maintenance_id
    def set_maintenance_id(self, v): self.__maintenance_id = v

    def get_equipment_id(self): return self.__equipment_id
    def set_equipment_id(self, v): self.__equipment_id = v

    def get_date_of_last_service(self): return self.__date_of_last_service
    def set_date_of_last_service(self, v): self.__date_of_last_service = v

    def get_equipment_type(self): return self.__equipment_type
    def set_equipment_type(self, v): self.__equipment_type = v

    def get_date_of_next_service(self): return self.__date_of_next_service
    def set_date_of_next_service(self, v): self.__date_of_next_service = v

    def get_operating_hours(self): return self.__operating_hours
    def set_operating_hours(self, v): self.__operating_hours = v

    def get_technician_grade(self): return self.__technician_grade
    def set_technician_grade(self, v): self.__technician_grade = v

    def get_maintenance_status(self): return self.__maintenance_status
    def set_maintenance_status(self, v): self.__maintenance_status = v

    def get_base_service_cost(self): return self.__base_service_cost
    def set_base_service_cost(self, v): self.__base_service_cost = v

    def get_parts_cost(self): return self.__parts_cost
    def set_parts_cost(self, v): self.__parts_cost = v

    def get_technician_fee(self): return self.__technician_fee
    def set_technician_fee(self, v): self.__technician_fee = v

    def get_overhaul_surcharge(self): return self.__overhaul_surcharge
    def set_overhaul_surcharge(self, v): self.__overhaul_surcharge = v

    def get_total_maintenance_cost(self): return self.__total_maintenance_cost
    def set_total_maintenance_cost(self, v): self.__total_maintenance_cost = v
