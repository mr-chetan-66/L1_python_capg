from datetime import datetime
import health_exception as he
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 8: continue
            if part[7] == 'Approved':
                cd = convert_date(part[5]); pd = convert_date(part[6])
                if (cd - pd).days <= 45:
                    records.append(line)
    return records

def validate_policy_id(policy_id):
    if len(policy_id) != 11:
        raise he.InvalidPolicyIdException(f"Invalid Policy Id: {policy_id}")
    if re.fullmatch(r"^POL-[A-Z]\d{2}-\d{3}$", policy_id): return True
    raise he.InvalidPolicyIdException(f"Invalid Policy Id: {policy_id}")

def validate_claim_id(claim_id):
    if len(claim_id) < 5:
        raise he.InvalidClaimIdException("Invalid Claim Id")
    if re.fullmatch(r"^CL\d{3,}$", claim_id): return True
    raise he.InvalidClaimIdException("Invalid Claim Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
