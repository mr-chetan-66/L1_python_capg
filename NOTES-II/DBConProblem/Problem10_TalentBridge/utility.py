# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import talent_exception as te
import re

def read_file(file):
    with open(file) as f:
        record=[]
        for line in f:
            part=line.strip().split(",")
            if part[8]=='Shortlisted':
                ad=convert_date(part[5])
                cd=convert_date(part[6])
                if (ad-cd).days<=15:
                    record.append(line)
        return record

def validate_job_code(job_code):
    if re.fullmatch(r"^JOB-[A-Z]{2}-[0-9]{4}$",job_code):
        return True
    else:
        raise te.InvalidJobCodeException(f"Invalid Job Code: {job_code}")

def validate_application_id(application_id):
    if re.fullmatch(r"^JA[0-9]{3,}$",application_id):
        return True
    else:
        raise te.InvalidJobCodeException("nvalid Application Id")

def convert_date(str_date):
    return datetime.strptime(str_date,"%d/%m/%Y").date()
