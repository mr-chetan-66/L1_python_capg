from datetime import date

class Shipment:
    def __init__(self, shipment_id:str, freight_id:str, client_name:str,
                 weight_kg:float, no_of_days:int, dispatch_date:date, service_type:str):
        self.__shipment_id = shipment_id
        self.__freight_id = freight_id
        self.__client_name = client_name
        self.__weight_kg = weight_kg
        self.__no_of_days = no_of_days
        self.__dispatch_date = dispatch_date
        self.__service_type = service_type
        self.__base_charge = 0.0
        self.__surcharge = 0.0
        self.__total_charge = 0.0

    def get_shipment_id(self): return self.__shipment_id
    def get_freight_id(self): return self.__freight_id
    def get_client_name(self): return self.__client_name
    def get_weight_kg(self): return self.__weight_kg
    def get_no_of_days(self): return self.__no_of_days
    def get_dispatch_date(self): return self.__dispatch_date
    def get_service_type(self): return self.__service_type
    def get_base_charge(self): return self.__base_charge
    def get_surcharge(self): return self.__surcharge
    def get_total_charge(self): return self.__total_charge

    def set_shipment_id(self, v): self.__shipment_id = v
    def set_freight_id(self, v): self.__freight_id = v
    def set_client_name(self, v): self.__client_name = v
    def set_weight_kg(self, v): self.__weight_kg = v
    def set_no_of_days(self, v): self.__no_of_days = v
    def set_dispatch_date(self, v): self.__dispatch_date = v
    def set_service_type(self, v): self.__service_type = v
    def set_base_charge(self, v): self.__base_charge = v
    def set_surcharge(self, v): self.__surcharge = v
    def set_total_charge(self, v): self.__total_charge = v

    def calculate_base_charge(self):
        base = self.__weight_kg * self.__no_of_days * 10.0
        if self.__weight_kg > 200:
            sur = base * 0.15
        elif self.__weight_kg > 100:
            sur = base * 0.08
        else:
            sur = 0.0
        self.__base_charge = base
        self.__surcharge = sur
        self.__total_charge = base + sur
        return sur
