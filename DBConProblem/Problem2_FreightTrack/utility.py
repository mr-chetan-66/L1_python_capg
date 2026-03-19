# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime,timedelta
import freight_exception as fe
import re

def read_file(file):
    record=[]
    with open(file) as f:
        for line in f:
            part=line.strip().split(",")
            if part[7]=='Dispatched':
                dd=convert_date(part[5])
                bd=convert_date(part[8])
                if((dd - bd).days)<=30:
                    record.append(line)
        
    return record          

def validate_freight_id(freight_id):
    if re.fullmatch(r"^FRT-\d{4}-[A-Z]{2}$",freight_id):
        return True
    else:
        raise fe.InvalidFreightIdException(f"Invalid Freight Id: {freight_id}")

def validate_shipment_id(shipment_id):
    if re.fullmatch(r"^SH\d{3,}$",shipment_id):
        return True
    else:
        raise fe.InvalidShipmentIdException("Invalid Shipment Id")

def convert_date(str_date):
    return datetime.strptime(str_date,"%d/%m/%Y").date()
