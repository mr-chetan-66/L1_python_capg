from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            insurance = parts[7]
            if insurance == 'Insured':
                doa = convert_date(parts[2])
                dod = convert_date(parts[4])
                if (dod - doa).days <= 90:
                    records.append(line)
    return records


def validate_bill_id(bill_id):
    if len(bill_id) < 4:
        raise ex.InvalidBillIdException("Invalid Bill Id")
    if re.fullmatch(r"^BIL\d+$", bill_id):
        return True
    else:
        raise ex.InvalidBillIdException("Invalid Bill Id")


def validate_ward_type(ward_type):
    valid_wards = ['General', 'Semi-Private', 'Private', 'ICU']
    if ward_type in valid_wards:
        return True
    else:
        raise ex.InvalidWardTypeException("Invalid Ward Type")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
