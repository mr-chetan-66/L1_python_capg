from datetime import datetime
import power_exception as pe
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 8:
                continue
            if part[7] == 'Active':
                reading = convert_date(part[5])
                billing = convert_date(part[6])
                if (reading - billing).days <= 15:
                    records.append(line)
    return records

def validate_meter_code(meter_code):
    if len(meter_code) != 12:
        raise pe.InvalidMeterCodeException(f"Invalid Meter Code: {meter_code}")
    if re.fullmatch(r"^MTR-[A-Z]\d{2}-\d{4}$", meter_code):
        return True
    raise pe.InvalidMeterCodeException(f"Invalid Meter Code: {meter_code}")

def validate_reading_id(reading_id):
    if len(reading_id) < 5:
        raise pe.InvalidReadingIdException("Invalid Reading Id")
    if re.fullmatch(r"^MR\d{3,}$", reading_id):
        return True
    raise pe.InvalidReadingIdException("Invalid Reading Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
