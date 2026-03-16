from datetime import datetime
import invalid_exception as ie
import re


def access_file(file):
    return open(file)

def validate_car_number(car_number):
    # Write your code here
    ## Fill your code here
    pattern = r"^NXF[0-9]{3}.{3}[a-zA-Z]$"
    if not re.fullmatch(pattern, car_number):
        raise ie.InvalidCarNumberException("Invalid Car Number")

    return True  # TODO: Remove this statement after writing your code

def convert_date(str_date):
    # Write your code here
    date_obj = datetime.strptime(str_date, "%d/%m/%Y")
    return date_obj  # TODO CHANGE THIS RETURN VALUE
