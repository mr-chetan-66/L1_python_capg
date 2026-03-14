class InvalidCarNumberException(Exception):
    #Create the constructor here  
    def __init__(self,message):
        super().__init__(message)