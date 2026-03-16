from datetime import datetime
import invalid_exception as ie
import re

def access_file(file):
    # Write your code here
    return open(file)


def validate_car_number(car_number):
    pattern=r"^NXF\d{3}.{3}[A-Za-z]$"
    if re.fullmatch(pattern,car_number):
        return True
    # else:
        
        # raise ie.InvalidCarNumberException("Invalid Car Number")
    
def convert_date(str_date):
    return datetime.strptime(str_date,"%d/%m/%Y").date()


    