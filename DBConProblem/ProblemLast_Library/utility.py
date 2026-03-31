### DO NOT ALTER THE GIVEN TEMPLATE. FILL CODE ONLY IN THE PROVIDED PLACES.

from datetime import datetime
import exception as ex
import re


def convert_date(str_date):
    return datetime.strptime(str_date, "%Y-%m-%d").date()


def validate_lending_id(lending_id):
    if re.fullmatch(r"L\d{3}",lending_id):
        return True
    else:
        raise ex.InvalidLendingIdException("Invalid Lending Id")


def read_file(file_path):
    # Write your code here
    with open(file_path) as f:
        record=[]
        for line in f:
            part=line.strip().split(",")
            if part[7]=='Paid':
                dd=convert_date(part[4])
                dl=convert_date(part[2])
                if ((dd-dl).days)<=365:
                    record.append(line)
                    
        return record
