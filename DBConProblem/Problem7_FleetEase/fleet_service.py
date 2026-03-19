# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import vehicle_service as vs
from datetime import timedelta
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
        # Write your code here
        # For each line in records:
        #   1. Validate vehicle_id — catch InvalidVehicleIdException and print message
        #   2. Validate service_id — catch InvalidServiceIdException and print message
        #   3. Convert service_date and booking_date
        #   4. Create VehicleService object
        #   5. Call calculate_service_cost() — store labour_cost in self.__labour_dict
        #   6. Call add_service_details() to insert into DB
        # Truncate the VehicleService table at the start.
        # Return None.
        pass

    def add_service_details(self, obj):
        # Write your code here
        # Insert VehicleService into 'VehicleService' table.
        # Column order: service_id, vehicle_id, vehicle_name, vehicle_type,
        #               odometer_km, service_date, booking_date,
        #               parts_cost, labour_cost, total_cost
        # Return None.
        pass

    def find_top3_vehicles(self):
        # Write your code here
        # Count how many times each vehicle_id appears in VehicleService table.
        # Return {vehicle_id: count} for top 3 distinct counts sorted descending.
        # Handle ties — all vehicle_ids within top 3 distinct values must be included.
        pass

    def search_service(self, service_id):
        # Write your code here
        # Query VehicleService table for given service_id.
        # Return fully populated VehicleService object, or None if not found.
        pass

    def find_high_mileage(self, start_date, end_date):
        # Write your code here
        # Find all services where:
        #   - odometer_km > 60000
        #   - service_date is between start_date and end_date (inclusive)
        # Return {service_id: odometer_km}. Return empty dict if none found.
        pass

    def update_labour_cost(self, vehicle_type):
        # Write your code here
        # For all services matching vehicle_type:
        #   UPDATE: labour_cost = labour_cost * 1.08
        #           total_cost = parts_cost + (labour_cost * 1.08)
        # After update, SELECT all services with that vehicle_type.
        # Return list of VehicleService objects, or None if none found.
        pass
