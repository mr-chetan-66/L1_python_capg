class Customer:
    def __init__(self,acc_no,cust_name,acc_type,acc_balance):
        self.__acc_no = acc_no
        self.__cust_name = cust_name
        self.__acc_type = acc_type
        self.__acc_balance = acc_balance
        
        
    def get_acc_no(self):
        return self.__acc_no
    def set_acc_no(self,acc_no):
        self.__acc_no = acc_no
        
    def get_cust_name(self):
        return self.__cust_name
    def set_cust_name(self,cust_name):
        self.__cust_name = cust_name
    
    def get_acc_type(self):
        return self.__acc_type
    def set_acc_type(self,acc_type):
        self.acc_type = acc_type
        
    def get_acc_balance(self):
        return self.__acc_balance
    def set_acc_balance(self,acc_balance):
        self.__acc_balance = acc_balance
        
        


