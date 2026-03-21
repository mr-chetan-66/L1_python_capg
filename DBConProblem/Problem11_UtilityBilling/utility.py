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
            uc=float(part[5])
            if uc>=50 and part[7]=='Pending':
                rd=convert_date(part[4])
                bd=convert_date(part[2])
                if ((rd-bd).days)<=60:
                    record.append(line)
        return record                
                


def validate_bill_id(bill_id):
    if re.fullmatch(r"^ENB[0-9]{3,}$",bill_id):
        return True
    else:
        raise ex.InvalidBillIdException("Invalid Bill Id")


def validate_consumer_type(consumer_type):
    if consumer_type in['Residential','Commercial','Industrial','Agricultural']:
        return True
    else:
        raise ex.InvalidConsumerTypeException("Invalid Customer Type")


def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()
