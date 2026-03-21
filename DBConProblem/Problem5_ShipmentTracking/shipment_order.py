# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import date

class ShipmentOrder:

    def __init__(self,shipment_id:str,sender_id:str,date_of_dispatch:date,zone:str,date_of_delivery:str,weight_in_kg:float,shipment_type:str,delivery_status:str):
        self.__shipment_id = shipment_id
        self.__sender_id = sender_id
        self.__date_of_dispatch = date_of_dispatch
        self.__zone = zone
        self.__date_of_delivery = date_of_delivery
        self.__weight_in_kg = weight_in_kg
        self.__shipment_type = shipment_type
        self.__delivery_status = delivery_status
        self.__freight_charge = 0.0
        self.__handling_charge = 0.0
        self.__delay_penalty = 0.0
        self.__tax = 0.0
        self.__total_shipping_cost = 0.0
    # Write all getters and setters for the private attributes below

    def get_shipment_id(self):
        return self.__shipment_id

    def set_shipment_id(self, shipment_id):
        self.__shipment_id = shipment_id

    def get_sender_id(self):
        return self.__sender_id

    def set_sender_id(self, sender_id):
        self.__sender_id = sender_id

    def get_date_of_dispatch(self):
        return self.__date_of_dispatch

    def set_date_of_dispatch(self, date_of_dispatch):
        self.__date_of_dispatch = date_of_dispatch

    def get_zone(self):
        return self.__zone

    def set_zone(self, zone):
        self.__zone = zone

    def get_date_of_delivery(self):
        return self.__date_of_delivery

    def set_date_of_delivery(self, date_of_delivery):
        self.__date_of_delivery = date_of_delivery

    def get_weight_in_kg(self):
        return self.__weight_in_kg

    def set_weight_in_kg(self, weight_in_kg):
        self.__weight_in_kg = weight_in_kg

    def get_shipment_type(self):
        return self.__shipment_type

    def set_shipment_type(self, shipment_type):
        self.__shipment_type = shipment_type

    def get_delivery_status(self):
        return self.__delivery_status

    def set_delivery_status(self, delivery_status):
        self.__delivery_status = delivery_status

    def get_freight_charge(self):
        return self.__freight_charge

    def set_freight_charge(self, freight_charge):
        self.__freight_charge = freight_charge

    def get_handling_charge(self):
        return self.__handling_charge

    def set_handling_charge(self, handling_charge):
        self.__handling_charge = handling_charge

    def get_delay_penalty(self):
        return self.__delay_penalty

    def set_delay_penalty(self, delay_penalty):
        self.__delay_penalty = delay_penalty

    def get_tax(self):
        return self.__tax

    def set_tax(self, tax):
        self.__tax = tax

    def get_total_shipping_cost(self):
        return self.__total_shipping_cost

    def set_total_shipping_cost(self, total_shipping_cost):
        self.__total_shipping_cost = total_shipping_cost
