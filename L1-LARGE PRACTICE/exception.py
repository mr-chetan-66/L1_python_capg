## Please do not change the skelecton code given here. Write your code only in the provided places alone.

class InvalidServiceIDException(Exception):
    message=""
    ## Create the constructor here
    def __init__(self, message):
        super().__init__(message)
        self.message= message
    
    
