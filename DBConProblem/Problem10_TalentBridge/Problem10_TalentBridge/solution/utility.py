from datetime import datetime
import talent_exception as te
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 9: continue
            if part[8] == 'Shortlisted':
                apd = convert_date(part[5]); cld = convert_date(part[6])
                if (apd - cld).days <= 15:
                    records.append(line)
    return records

def validate_job_code(job_code):
    if len(job_code) != 11:
        raise te.InvalidJobCodeException(f"Invalid Job Code: {job_code}")
    if re.fullmatch(r"^JOB-[A-Z]{2}-\d{4}$", job_code): return True
    raise te.InvalidJobCodeException(f"Invalid Job Code: {job_code}")

def validate_application_id(application_id):
    if len(application_id) < 5:
        raise te.InvalidApplicationIdException("Invalid Application Id")
    if re.fullmatch(r"^JA\d{3,}$", application_id): return True
    raise te.InvalidApplicationIdException("Invalid Application Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
