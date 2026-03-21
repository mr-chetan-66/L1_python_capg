# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class ShipmentOrder:

    # Define the parameterized constructor here
    # Parameters: shipment_id, sender_id, date_of_dispatch, zone,
    #             date_of_delivery, weight_in_kg, shipment_type, delivery_status
    # Default values for remaining cost attributes: 0.0
    def __init__(self, shipment_id: str, sender_id: str, date_of_dispatch: date,
                 zone: str, date_of_delivery: date, weight_in_kg: float,
                 shipment_type: str, delivery_status: str):
        # Write your code here
        pass

    # Write all getters and setters for the private attributes below

    def get_shipment_id(self):
        pass

    def set_shipment_id(self, shipment_id):
        pass

    def get_sender_id(self):
        pass

    def set_sender_id(self, sender_id):
        pass

    def get_date_of_dispatch(self):
        pass

    def set_date_of_dispatch(self, date_of_dispatch):
        pass

    def get_zone(self):
        pass

    def set_zone(self, zone):
        pass

    def get_date_of_delivery(self):
        pass

    def set_date_of_delivery(self, date_of_delivery):
        pass

    def get_weight_in_kg(self):
        pass

    def set_weight_in_kg(self, weight_in_kg):
        pass

    def get_shipment_type(self):
        pass

    def set_shipment_type(self, shipment_type):
        pass

    def get_delivery_status(self):
        pass

    def set_delivery_status(self, delivery_status):
        pass

    def get_freight_charge(self):
        pass

    def set_freight_charge(self, freight_charge):
        pass

    def get_handling_charge(self):
        pass

    def set_handling_charge(self, handling_charge):
        pass

    def get_delay_penalty(self):
        pass

    def set_delay_penalty(self, delay_penalty):
        pass

    def get_tax(self):
        pass

    def set_tax(self, tax):
        pass

    def get_total_shipping_cost(self):
        pass

    def set_total_shipping_cost(self, total_shipping_cost):
        pass
