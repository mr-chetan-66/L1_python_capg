### tracking_event.py
### Entity class for TrackingEvent

class TrackingEvent:
    def __init__(self, event_id, shipment_id, event_datetime,
                 location, event_description):
        self.__event_id          = event_id
        self.__shipment_id       = shipment_id
        self.__event_datetime    = event_datetime    # datetime.datetime object
        self.__location          = location
        self.__event_description = event_description

    def get_event_id(self):
        return self.__event_id

    def set_event_id(self, v):
        self.__event_id = v

    def get_shipment_id(self):
        return self.__shipment_id

    def set_shipment_id(self, v):
        self.__shipment_id = v

    def get_event_datetime(self):
        return self.__event_datetime

    def set_event_datetime(self, v):
        self.__event_datetime = v

    def get_location(self):
        return self.__location

    def set_location(self, v):
        self.__location = v

    def get_event_description(self):
        return self.__event_description

    def set_event_description(self, v):
        self.__event_description = v
