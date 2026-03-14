class train:
    def __init__(self,train_number,train_name,source,destination,ac1,ac2,ac3,sleeper,seater):
        self.__train_number = train_number
        self.__train_name = train_name
        self.__source = source
        self.__destination = destination
        self.__ac1 = ac1
        self.__ac2 = ac2
        self.__ac3 = ac3
        self.__sleeper = sleeper
        self.__seater= seater
       
    def get_train_number(self):
        return self.__train_number
   
    def set_train_number(self,train_number):
        self.__train_number = train_number
   
    def get_train_name(self):
        return self.__train_name
   
    def set_train_name(self,train_name):
        self.__train_name = train_name
   
    def get_source(self):
        return self.__source
       
    def set_source(self,source):
        self.__source = source
   
    def get_destination(self):
        return self.__destination
       
    def set_destination(self,destination):
        self.destination = destination
       
    def get_ac1(self):
        return self.__ac1
       
    def set_ac1(self,ac1):
        self.__ac1 = ac1
   
    def get_ac2(self):
        return self.__ac2
       
    def set_ac2(self,ac2):
        self.__ac2 = ac2
   
    def get_ac3(self):
        return self.__ac3
       
    def set_ac3(self,ac3):
        self.__ac3 = ac3
       
    def get_sleeper(self):
        return self.__sleeper
       
    def set_sleeper(self,sleeper):
        self.__sleeper = sleeper
   
    def get_seater(self):
        return self.__seater
       
    def set_seater(self,seater):
        self.__seater = seater