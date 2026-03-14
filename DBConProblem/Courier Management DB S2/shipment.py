### shipment.py
### Entity class for Shipment

class Shipment:
    def __init__(self, shipment_id, tracking_number, sender_name,
                 receiver_name, origin_city, destination_city,
                 dispatch_date, expected_delivery_date, weight_kg,
                 status):
        self.__shipment_id            = shipment_id
        self.__tracking_number        = tracking_number
        self.__sender_name            = sender_name
        self.__receiver_name          = receiver_name
        self.__origin_city            = origin_city
        self.__destination_city       = destination_city
        self.__dispatch_date          = dispatch_date           # datetime.date
        self.__expected_delivery_date = expected_delivery_date  # datetime.date
        self.__weight_kg              = weight_kg               # float
        self.__status                 = status
        # status values: 'Booked', 'In Transit', 'Out for Delivery',
        #                'Delivered', 'Returned'

    def get_shipment_id(self):
        return self.__shipment_id

    def set_shipment_id(self, v):
        self.__shipment_id = v

    def get_tracking_number(self):
        return self.__tracking_number

    def set_tracking_number(self, v):
        self.__tracking_number = v

    def get_sender_name(self):
        return self.__sender_name

    def set_sender_name(self, v):
        self.__sender_name = v

    def get_receiver_name(self):
        return self.__receiver_name

    def set_receiver_name(self, v):
        self.__receiver_name = v

    def get_origin_city(self):
        return self.__origin_city

    def set_origin_city(self, v):
        self.__origin_city = v

    def get_destination_city(self):
        return self.__destination_city

    def set_destination_city(self, v):
        self.__destination_city = v

    def get_dispatch_date(self):
        return self.__dispatch_date

    def set_dispatch_date(self, v):
        self.__dispatch_date = v

    def get_expected_delivery_date(self):
        return self.__expected_delivery_date

    def set_expected_delivery_date(self, v):
        self.__expected_delivery_date = v

    def get_weight_kg(self):
        return self.__weight_kg

    def set_weight_kg(self, v):
        self.__weight_kg = v

    def get_status(self):
        return self.__status

    def set_status(self, v):
        self.__status = v
