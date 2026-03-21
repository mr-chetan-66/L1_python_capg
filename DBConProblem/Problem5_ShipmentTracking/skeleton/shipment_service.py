### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

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
        """
        Call utility.read_file() with input_file.
        Pass the result to build_shipment_list().
        Return __shipment_list.
        """
        # Write your code here
        pass

    def build_shipment_list(self, records):
        """
        For each record string:
          1. Validate shipment_id  -> catch InvalidShipmentIdException, print the message
          2. Validate zone         -> catch InvalidZoneException, print the message
          3. Convert date strings using utility.convert_date()
          4. Create a ShipmentOrder object
          5. Call calculate_shipping_costs() and set all cost attributes
          6. Append the object to __shipment_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_shipping_costs(self, weight_in_kg, zone, date_of_dispatch, date_of_delivery):
        """
        Return [freight_charge, handling_charge, delay_penalty, tax, total_shipping_cost].

        Zone-based rates (per kg):
        +--------+----------------+-----------------+-------+
        | Zone   | Freight/kg(INR)| Handling/kg(INR)| Tax % |
        +--------+----------------+-----------------+-------+
        | Zone_A |      50        |       10        |  5%   |
        | Zone_B |      80        |       15        |  8%   |
        | Zone_C |     120        |       20        |  10%  |
        | Zone_D |     200        |       30        |  12%  |
        +--------+----------------+-----------------+-------+

        freight_charge   = freight_rate_per_kg * weight_in_kg
        handling_charge  = handling_rate_per_kg * weight_in_kg
        gross            = freight_charge + handling_charge
        tax              = gross * tax_pct / 100
        delay_penalty    = weight_in_kg * 25.0  if transit_days > 7  else  0.0
                           (transit_days = (date_of_delivery - date_of_dispatch).days)
        total_shipping_cost = gross + tax + delay_penalty
        """
        # Write your code here
        pass

    def add_shipment_details(self, shipment_list):
        """
        Insert each ShipmentOrder object in shipment_list into the
        'shipment_order' table.
        Column order: shipment_id, sender_id, date_of_dispatch, zone,
                      date_of_delivery, weight_in_kg, shipment_type, delivery_status,
                      freight_charge, handling_charge, delay_penalty, tax,
                      total_shipping_cost
        Returns None.
        """
        # Write your code here
        pass

    def search_shipment(self, shipment_id):
        """
        Query 'shipment_order' by shipment_id.
        If found, build and return a fully populated ShipmentOrder object.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_freight(self, weight_threshold):
        """
        For all records where weight_in_kg > weight_threshold:
          - Increase freight_charge by 20%
          - Recalculate total_shipping_cost = new_freight + handling_charge + tax + delay_penalty
        Commit the update. Fetch and return all updated ShipmentOrder objects as a list.
        Return None if no records qualify.
        """
        # Write your code here
        pass
