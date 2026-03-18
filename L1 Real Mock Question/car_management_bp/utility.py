from datetime import datetime
import invalid_exception as ie
import re

def access_file(file):
   return open(file)

def validate_car_number(car_number):
    if re.fullmatch(r"^NXF\d{3}.{3}[A-Za-z]$",car_number):
        return True
    else:
        raise ie.InvalidCarNumberException("Invalid Car Number")
    
def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()


    