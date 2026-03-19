# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class VehicleService:

    def __init__(self, service_id:str, vehicle_id:str, vehicle_name:str,
                 vehicle_type:str, odometer_km:int, service_date:date, booking_date:date):
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
        # Write your code here
        # Business Rule — Cost tiers by vehicle_type AND odometer_km:
        #
        # Truck:
        #   odometer_km <= 50000  -> parts_cost = 8000.0,  labour_cost = 3000.0
        #   odometer_km <= 80000  -> parts_cost = 14000.0, labour_cost = 5000.0
        #   odometer_km > 80000   -> parts_cost = 22000.0, labour_cost = 8000.0
        #
        # Bus:
        #   odometer_km <= 60000  -> parts_cost = 10000.0, labour_cost = 4000.0
        #   odometer_km <= 90000  -> parts_cost = 18000.0, labour_cost = 6500.0
        #   odometer_km > 90000   -> parts_cost = 28000.0, labour_cost = 10000.0
        #
        # Van:
        #   odometer_km <= 30000  -> parts_cost = 3000.0,  labour_cost = 1500.0
        #   odometer_km <= 50000  -> parts_cost = 6000.0,  labour_cost = 2500.0
        #   odometer_km > 50000   -> parts_cost = 10000.0, labour_cost = 4000.0
        #
        # Car:
        #   odometer_km <= 20000  -> parts_cost = 1500.0,  labour_cost = 800.0
        #   odometer_km <= 40000  -> parts_cost = 3500.0,  labour_cost = 1500.0
        #   odometer_km > 40000   -> parts_cost = 6000.0,  labour_cost = 2500.0
        #
        # total_cost = parts_cost + labour_cost
        # Set all three fields. Return labour_cost.
        pass
