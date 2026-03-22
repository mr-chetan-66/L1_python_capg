from datetime import datetime
import exception as ex
import re

def read_file(file):
    with open(file) as f:
        request=[]
        for line in f:
            part=line.strip().split(",")
            ap=part[7]
            if ap=='Approved':
                dor=convert_date(part[2])
                dot=convert_date(part[4])
                diff=(dor-dot).days
                if(diff<180):
                    request.append(line)
        return request
    
def validate_request_id(request_id):
    try:
        if re.fullmatch(r"^R00[0-9]+$",request_id):
            return True
        else:
            raise ex.InvalidRequestIdException("Invalid Request Id")
    except ex.InvalidRequestIdException as e:
        return e.message
    
def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()





