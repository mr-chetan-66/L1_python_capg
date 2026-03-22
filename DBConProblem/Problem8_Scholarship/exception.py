# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

class InvalidApplicationIdException(Exception):
    # Write the constructor and get_message method here
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        # Write your code here
        return self.__message


class InvalidCourseTypeException(Exception):
    # Write the constructor and get_message method here
    def __init__(self, message):
        super().__init__(message)
        self.__message=message

    def get_message(self):
        # Write your code here
        return self.__message
