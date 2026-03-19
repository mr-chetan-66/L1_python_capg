# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
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
        # Write your code here
        # For each line in records:
        #   1. Validate freight_id - catch InvalidFreightIdException and print message
        #   2. Validate shipment_id - catch InvalidShipmentIdException and print message
        #   3. Convert dispatch_date using utility
        #   4. Create Shipment object
        #   5. Call calculate_base_charge() on the object
        #   6. Call add_shipment_details() to insert into DB
        #   7. If surcharge > 0, store {shipment_id: surcharge} in self.__surcharge_dict
        # Truncate the Shipment table at the start.
        # Return None.
        pass

    def add_shipment_details(self, obj):
        # Write your code here
        # Insert the Shipment object into the 'Shipment' table.
        # Column order: shipment_id, freight_id, client_name, weight_kg, no_of_days,
        #               dispatch_date, service_type, base_charge, surcharge, total_charge
        # Return None.
        pass

    def find_top3_freight(self):
        # Write your code here
        # Count how many times each freight_id appears in the Shipment table.
        # Identify the top 3 distinct usage counts.
        # Return a dict {freight_id: count} sorted by count descending.
        # All freight IDs whose count falls within the top 3 distinct count values must be included.
        pass

    def search_shipment(self, shipment_id):
        # Write your code here
        # Query the Shipment table for the given shipment_id.
        # Build and return a fully populated Shipment object, or None if not found.
        pass

    def find_delivery_dates(self, start_date, end_date):
        # Write your code here
        # Find all shipments where:
        #   - no_of_days > 4
        #   - dispatch_date is between start_date and end_date (inclusive)
        # Delivery date = dispatch_date + no_of_days (timedelta)
        # Return {shipment_id: delivery_date}. Return empty dict if none found.
        pass

    def update_surcharge(self, service_type):
        # Write your code here
        # For all shipments matching service_type:
        #   UPDATE: surcharge = surcharge * 1.12
        #           total_charge = base_charge + (surcharge * 1.12)
        # After update, SELECT all shipments with that service_type.
        # Build and return a list of Shipment objects with updated values.
        # Return None if no records found.
        pass
