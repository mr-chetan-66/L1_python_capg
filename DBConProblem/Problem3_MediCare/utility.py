# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import med_exception as me
import re

def read_file(file):
    record=[]
    with open(file) as f:
        for line in f:
            part=line.strip().split(",")
            if part[8]=='Verified':
                ed=convert_date(part[7])
                md=convert_date(part[6])
                if ed>md:
                    record.append(line)
    return record
            
def validate_med_code(med_code):
    if re.fullmatch(r"^MED-[A-Z]\d{3}-R[A-Z]$",med_code):
        return True
    else:
        raise me.InvalidMedCodeException(f"Invalid Med Code: {med_code}")

def validate_stock_id(stock_id):
    if re.fullmatch(r"^MD\d{3,}$",stock_id):
        return True
    else:
        raise me.InvalidStockIdException("Invalid Stock Id")

def convert_date(str_date):
    return datetime.strptime(str_date,"%d/%m/%Y").date()
