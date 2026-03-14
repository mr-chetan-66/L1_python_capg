### vehicle.py
### Entity class for Vehicle

class Vehicle:
    def __init__(self, vehicle_id, owner_name, vehicle_type, brand, model, registration_year, insurance_expiry):
        self.__vehicle_id        = vehicle_id
        self.__owner_name        = owner_name
        self.__vehicle_type      = vehicle_type
        self.__brand             = brand
        self.__model             = model
        self.__registration_year = registration_year
        self.__insurance_expiry  = insurance_expiry

    def get_vehicle_id(self):
        return self.__vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.__vehicle_id = vehicle_id

    def get_owner_name(self):
        return self.__owner_name

    def set_owner_name(self, owner_name):
        self.__owner_name = owner_name

    def get_vehicle_type(self):
        return self.__vehicle_type

    def set_vehicle_type(self, vehicle_type):
        self.__vehicle_type = vehicle_type

    def get_brand(self):
        return self.__brand

    def set_brand(self, brand):
        self.__brand = brand

    def get_model(self):
        return self.__model

    def set_model(self, model):
        self.__model = model

    def get_registration_year(self):
        return self.__registration_year

    def set_registration_year(self, registration_year):
        self.__registration_year = registration_year

    def get_insurance_expiry(self):
        return self.__insurance_expiry

    def set_insurance_expiry(self, insurance_expiry):
        self.__insurance_expiry = insurance_expiry
