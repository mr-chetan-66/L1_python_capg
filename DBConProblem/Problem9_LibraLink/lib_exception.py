class InvalidBookCodeException(Exception):
    def __init__(self, message):
        pass
    def get_message(self): return self.__message

class InvalidIssueIdException(Exception):
    def __init__(self, message):
        pass
    def get_message(self): return self.__message
