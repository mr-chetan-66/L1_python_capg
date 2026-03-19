from datetime import datetime
import med_exception as me
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 9:
                continue
            status = part[8]
            if status == 'Verified':
                exp = convert_date(part[7])
                mfg = convert_date(part[6])
                if exp > mfg:
                    records.append(line)
    return records

def validate_med_code(med_code):
    if len(med_code) != 12:
        raise me.InvalidMedCodeException(f"Invalid Med Code: {med_code}")
    if re.fullmatch(r"^MED-[A-Z]\d{3}-RX$", med_code):
        return True
    raise me.InvalidMedCodeException(f"Invalid Med Code: {med_code}")

def validate_stock_id(stock_id):
    if len(stock_id) < 5:
        raise me.InvalidStockIdException("Invalid Stock Id")
    if re.fullmatch(r"^MD\d{3,}$", stock_id):
        return True
    raise me.InvalidStockIdException("Invalid Stock Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
