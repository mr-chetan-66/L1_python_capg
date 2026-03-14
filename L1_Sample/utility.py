## Please do not change the skelecton code given here. Write your code only in the provided places alone.

import it_service_management as itsm
from datetime import datetime,date
import exception as ex
import re

def read_file(file):
    ## Write your code here
    record=[]
    with open("input.txt","r") as f:
        for line in f:
            line=line.strip()
            
            if not line:
                continue
            
            part=line.split(":")
            if len(part)==5:
                record.append(part)
                
    return record

def validate_service_id(service_id):
    pattern=r'^ITSERVICE/\d{4}$'
    if re.match(pattern,service_id):
        return True
    else:
        raise ex.InvalidServiceIDException("Invalid Service ID")
    
def convert_date(str_date):
    # Write your code here
    return datetime.strptime(str_date,"%Y-%m-%d").date()

