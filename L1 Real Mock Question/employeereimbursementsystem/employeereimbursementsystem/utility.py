from datetime import date,datetime,timedelta
import exception as ex
import re

#correct
def read_file(file):
    request=[]
    with open(file) as f:
        for line in f:
            part=line.strip().split(",")
            app=part[7]
            if app=='Approved':
                dor=convert_date(part[2])
                dot=convert_date(part[4])
                if ((dor-dot).days)<180:
                    request.append(line)
    return request

def validate_request_id(request_id):
    if len(request_id)<4:
        raise ex.InvalidRequestIdException("Invalid Request Id")
    
    if re.fullmatch(r"^R00\d+$",request_id):
        return True
    else:
        raise ex.InvalidRequestIdException("Invalid Request Id")
    
def convert_date(str_date):
    y,m,d=map(int,str_date.split("-"))
    return date(y,m,d)
