# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import datetime
import exception as ex
import re


def read_file(file):
    with open(file) as f:
        record=[]
        for line in f:
            part=line.strip().split(",")
            if part[8]=='Eligible' and float(part[5])>6.0:
                da=convert_date(part[2])
                de=convert_date(part[4])
                if ((da-de).days)<=120:
                    record.append(line)             
                   
        return record


def validate_application_id(application_id):
    if re.fullmatch(r"SCH[0-9]{3,}",application_id):
        return True
    else:
        raise ex.InvalidApplicationIdException("Invalid Application Id")
    
def validate_course_type(course_type):
    if course_type in ['UG','PG','Diploma','PhD']:
        return True
    else:
        raise ex.InvalidCourseTypeException("Invalid Course Type")

def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()
