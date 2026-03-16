class InvalidCarNumberException(Exception):
    message = ""
    #Create the constructor here  
    def __init__(self, message):
        super().__init__(message)
        self.message=message
   