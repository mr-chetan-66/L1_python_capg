# Please do not change the skeleton code given here.
# Write your code only in the provided places alone

from datetime import datetime
import re
import exception as ex

def read_file(file):
    with open(file) as f:
        record=[]
        for line in f:
            part=line.strip().split(",")
            if part[7]=="Delivered":
                dlv=convert_date(part[4])
                dtp=convert_date(part[2])
                
                if ((dlv-dtp).days)<=60:
                    record.append(line)
        return record 


def validate_shipment_id(shipment_id):
    if re.fullmatch(r"^SHP[0-9]+$",shipment_id):
        return True
    else:
        raise ex.InvalidShipmentIdException("Invalid Shipment Id")

def validate_zone(zone):
    if zone in ['Zone_A','Zone_B','Zone_C','Zone_D']:
        return True
    else:
        raise ex.InvalidShipmentIdException("Invalid Zone")


def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()
