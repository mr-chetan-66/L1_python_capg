## Please do not change the skelecton code given here. Write your code only in the provided places alone.

class ITService:
    ## Define the parameterized constructor here
    def __init__(self, service_id, customer_name, service_date, service_type, base_charge):
        self.__service_id = service_id
        self.__customer_name = customer_name
        self.__service_date = service_date
        self.__service_type = service_type
        self.__base_charge = base_charge
        self.__service_charge  = 0.0
    
    ## Getters and Setters
    def set_service_id(self, service_id):
        self.__service_id = service_id
        
    def get_service_id(self):
        return self.__service_id
    
    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name
        
    def get_customer_name(self):
        return self.__customer_name
    
    def set_service_date(self, service_date):
        self.__service_date = service_date
        
    def get_service_date(self):
        return self.__service_date
    
    def set_service_type(self, service_type):
        self.__service_type = service_type
        
    def get_service_type(self):
        return self.__service_type

    def set_base_charge(self, base_charge):
        self.__base_charge = base_charge

    def get_base_charge(self):
        return self.__base_charge
    
    def set_service_charge(self, service_charge):
        self.__service_charge = service_charge
        
    def get_service_charge(self):
        return self.__service_charge

    def calculate_service_charge(self):
        ## Write your code here
        extra_charges = 4700.0
        vals = {"Software Development": 5000.0, "Technical Support": 4000.0, "Data Analysis": 7000.0}
        if self.__service_type in vals.keys():
            extra_charges = vals[self.__service_type]
        total = float(self.__base_charge) + extra_charges
        self.__service_charge = total
        

        
            