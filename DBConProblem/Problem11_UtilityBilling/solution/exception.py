class InvalidBillIdException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message


class InvalidConsumerTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message
