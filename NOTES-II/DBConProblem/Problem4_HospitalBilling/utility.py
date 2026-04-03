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
            if part[7]=='Insured':
                da=convert_date(part[2])
                dd=convert_date(part[4])
                if ((dd-da).days)<=90:
                    record.append(line)
        return record


def validate_bill_id(bill_id):
    if re.fullmatch(r"^BIL[0-9]+$",bill_id):
        return True
    else:
        raise ex.InvalidBillIdException("Invalid Bill Id")

def validate_ward_type(ward_type):
    if ward_type in ['General','Semi-Private','Private','ICU']:
        return True
    else:
        raise ex.InvalidWardTypeException("Invalid Ward Type")


def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()
