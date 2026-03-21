# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

class InvalidBillIdException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        self.__message


class InvalidConsumerTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        self.__message
