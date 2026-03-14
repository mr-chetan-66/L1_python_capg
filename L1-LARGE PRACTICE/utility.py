## Please do not change the skelecton code given here. Write your code only in the provided places alone.

import it_service_management as itsm
from datetime import datetime,date
import exception as ex
import re
def read_file(file):
    ## Write your code here
    result_list = []
    with open(file,"r") as file:
        for line in file:
            line = line.strip()
            data = line.split(":")
            result_list.append(data)
    
    return result_list

def validate_service_id(service_id):
    pattern = "^ITSERVICE/[0-9]{4}$"
    try: 
        if not re.match(pattern,service_id):
            raise ex.InvalidServiceIDException(f"Invalid Service Id - {service_id}")
        else :
            return True
    except ex.InvalidServiceIDException as e:
        print(e)
    
def convert_date(str_date):
    # Write your code here
    date_obj = datetime.strptime(str_date,"%Y-%m-%d")
    return date_obj.date()
    

# read_file("input.txt")