class InvalidApplicationIdException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message


class InvalidCourseTypeException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message
