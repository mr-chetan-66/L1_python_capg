## Please do not change the skelecton code given here. Write your code only in the provided places alone.

import it_service_management as itsm
from datetime import datetime,date
import exception as ex
import re
def read_file(file):
    ## Write your code here
    with open(file) as f:
        data = f.read().split("\n")
        lst = []
        for datum in data:
            vals = datum.split(":")
            lst.append(vals)
    return lst

def validate_service_id(service_id):
    try:
        ## Write your code here
        pattern = r"^ITSERVICE/[\d]{4}$"
        if re.match(pattern, service_id):
            return True
        raise ex.InvalidServiceIDException("Invalid Serive ID")
        
    except ex.InvalidServiceIDException as e:
        ## Write your code here
        return e.message
    
def convert_date(str_date):
    ## Write your code here
    
    return datetime.strptime(str_date, r"%Y-%m-%d").date()
   

# print(convert_date("2020-12-20"))