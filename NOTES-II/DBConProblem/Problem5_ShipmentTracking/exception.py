# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

class InvalidShipmentIdException(Exception):
    # Write the constructor and get_message method here
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        return self.__message


class InvalidZoneException(Exception):
    # Write the constructor and get_message method here
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        return self.__message
