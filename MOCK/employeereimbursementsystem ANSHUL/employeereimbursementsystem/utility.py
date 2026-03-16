from datetime import date,datetime,timedelta
import exception as ex
import re

#correct
def read_file(file):
    rec_list=[]
    with open( file,"r") as f:
        for line in f:
            line_list=line.strip().split(",")
            manager=line_list[7]
            date_travel=convert_date(line_list[4])
            date_now=date.today()
            diff=(date_travel-date_now).days
            if manager.lower()=="approved" and diff<=180:
                rec_list.append(line)

    return rec_list
 #TODO CHANGE THIS RETURN VALUE


def validate_request_id(request_id):
    try:
        pattern="^R00[0-9]$"
        if re.match(pattern,request_id):
            return True
        else:
            raise ex.InvalidRequestIdException("Invalid Request Id")
    except ex.InvalidRequestIdException as e:
        pass

    # try:
    #     if int(request_id[1])==0 and int(request_id[2])==0:
    #         return True
    #     elif type(int(request_id[3]))==type(2):
    #         return True
    #     elif len(request_id)>3:
    #         return True
    #     elif request_id[0]=="R":
    #         return True
    #     else:
    #         raise ex.InvalidRequestIdException("Invalid Request Id")
    # except ex.InvalidRequestIdException as e:
    #     print(e)
       
    
   

#correct
def convert_date(str_date):
    # Write your code here to conver the string to date
    converted_date= datetime.strptime(str_date,"%Y-%m-%d").date()
    return converted_date
    
    
    return None  #TODO CHANGE THIS RETURN VALUE

