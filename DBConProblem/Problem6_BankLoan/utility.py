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
            if part[8]=='Approved':
                dd=convert_date(part[4])
                da=convert_date(part[2])
                if ((dd-da).days)<=30:
                    record.append(line)
        return record 
            
def validate_loan_id(loan_id):
    if re.fullmatch(r"^LN[0-9]{3,}$",loan_id):
        return True
    else:
        raise ex.InvalidLoanIdException("Invalid Loan Id")
    


def validate_loan_type(loan_type):
    if loan_type in ['Home','Vehicle','Personal','Education']:
        return True
    else:
        raise ex.InvalidLoanIdException("Invalid Loan Type")


def convert_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d").date()
