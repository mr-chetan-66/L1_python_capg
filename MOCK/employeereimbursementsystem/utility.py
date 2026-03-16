from datetime import date
import exception as ex
import re

def read_file(file):
    f=open(file,"r")
    request=[]
    for line in file:
        part=line.split(",")
        ap=part[6] #[7]
        if ap=='Approved':
            dor=convert_date(part[4])
            dot=convert_date(part[2])
            diff=abs((dor-dot).days)
            if(diff<180):
                request.append(line)
    f.close()
    return request
    
def validate_request_id(request_id):
    try:
        pattern=r"^R00\d$"
        if len(request_id<4): #<4
            raise ex.InvalidRequestIdException("Invalid request Id")
        if re.fullmatch(pattern,request_id):
            return True
        else:
            raise ex.InvalidRequestIdException("Invalid request Id")
        
    except ex.InvalidRequestIdException as e:
        return e
    
def convert_date(str_date):
    #return date.strptime(str_date,"%Y-%m-%d") ##MANDAR
    y,m,d=map(int,str_date.split("-"))
    dt=date(y,m,d)
    return dt






