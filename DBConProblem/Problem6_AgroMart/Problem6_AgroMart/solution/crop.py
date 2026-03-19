from datetime import date

SEASON_RATES = {"Kharif": 0.15, "Rabi": 0.10, "Summer": 0.05}

class Crop:
    def __init__(self, agri_id, crop_code, crop_name, crop_type,
                 base_price, quantity_kg, season, harvest_date, listing_date):
        self.__agri_id = agri_id
        self.__crop_code = crop_code
        self.__crop_name = crop_name
        self.__crop_type = crop_type
        self.__base_price = base_price
        self.__quantity_kg = quantity_kg
        self.__season = season
        self.__harvest_date = harvest_date
        self.__listing_date = listing_date
        self.__seasonal_premium = 0.0
        self.__selling_price = 0.0
        self.__total_value = 0.0

    def get_agri_id(self): return self.__agri_id
    def get_crop_code(self): return self.__crop_code
    def get_crop_name(self): return self.__crop_name
    def get_crop_type(self): return self.__crop_type
    def get_base_price(self): return self.__base_price
    def get_quantity_kg(self): return self.__quantity_kg
    def get_season(self): return self.__season
    def get_harvest_date(self): return self.__harvest_date
    def get_listing_date(self): return self.__listing_date
    def get_seasonal_premium(self): return self.__seasonal_premium
    def get_selling_price(self): return self.__selling_price
    def get_total_value(self): return self.__total_value

    def set_agri_id(self, v): self.__agri_id = v
    def set_crop_code(self, v): self.__crop_code = v
    def set_crop_name(self, v): self.__crop_name = v
    def set_crop_type(self, v): self.__crop_type = v
    def set_base_price(self, v): self.__base_price = v
    def set_quantity_kg(self, v): self.__quantity_kg = v
    def set_season(self, v): self.__season = v
    def set_harvest_date(self, v): self.__harvest_date = v
    def set_listing_date(self, v): self.__listing_date = v
    def set_seasonal_premium(self, v): self.__seasonal_premium = v
    def set_selling_price(self, v): self.__selling_price = v
    def set_total_value(self, v): self.__total_value = v

    def calculate_selling_price(self):
        rate = SEASON_RATES.get(self.__season, 0.0)
        premium = self.__base_price * rate
        selling = self.__base_price + premium
        total = selling * self.__quantity_kg
        self.__seasonal_premium = premium
        self.__selling_price = selling
        self.__total_value = total
        return premium
