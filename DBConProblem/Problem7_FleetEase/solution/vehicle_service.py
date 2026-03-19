from datetime import date

class VehicleService:
    def __init__(self, service_id, vehicle_id, vehicle_name, vehicle_type,
                 odometer_km, service_date, booking_date):
        self.__service_id = service_id
        self.__vehicle_id = vehicle_id
        self.__vehicle_name = vehicle_name
        self.__vehicle_type = vehicle_type
        self.__odometer_km = odometer_km
        self.__service_date = service_date
        self.__booking_date = booking_date
        self.__parts_cost = 0.0
        self.__labour_cost = 0.0
        self.__total_cost = 0.0

    def get_service_id(self): return self.__service_id
    def get_vehicle_id(self): return self.__vehicle_id
    def get_vehicle_name(self): return self.__vehicle_name
    def get_vehicle_type(self): return self.__vehicle_type
    def get_odometer_km(self): return self.__odometer_km
    def get_service_date(self): return self.__service_date
    def get_booking_date(self): return self.__booking_date
    def get_parts_cost(self): return self.__parts_cost
    def get_labour_cost(self): return self.__labour_cost
    def get_total_cost(self): return self.__total_cost

    def set_service_id(self, v): self.__service_id = v
    def set_vehicle_id(self, v): self.__vehicle_id = v
    def set_vehicle_name(self, v): self.__vehicle_name = v
    def set_vehicle_type(self, v): self.__vehicle_type = v
    def set_odometer_km(self, v): self.__odometer_km = v
    def set_service_date(self, v): self.__service_date = v
    def set_booking_date(self, v): self.__booking_date = v
    def set_parts_cost(self, v): self.__parts_cost = v
    def set_labour_cost(self, v): self.__labour_cost = v
    def set_total_cost(self, v): self.__total_cost = v

    def calculate_service_cost(self):
        km = self.__odometer_km
        vt = self.__vehicle_type
        if vt == "Truck":
            if km <= 50000:   pc, lc = 8000.0, 3000.0
            elif km <= 80000: pc, lc = 14000.0, 5000.0
            else:             pc, lc = 22000.0, 8000.0
        elif vt == "Bus":
            if km <= 60000:   pc, lc = 10000.0, 4000.0
            elif km <= 90000: pc, lc = 18000.0, 6500.0
            else:             pc, lc = 28000.0, 10000.0
        elif vt == "Van":
            if km <= 30000:   pc, lc = 3000.0, 1500.0
            elif km <= 50000: pc, lc = 6000.0, 2500.0
            else:             pc, lc = 10000.0, 4000.0
        else:  # Car
            if km <= 20000:   pc, lc = 1500.0, 800.0
            elif km <= 40000: pc, lc = 3500.0, 1500.0
            else:             pc, lc = 6000.0, 2500.0
        self.__parts_cost = pc
        self.__labour_cost = lc
        self.__total_cost = pc + lc
        return lc
