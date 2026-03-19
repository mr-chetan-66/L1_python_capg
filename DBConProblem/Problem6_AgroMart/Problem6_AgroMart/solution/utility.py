from datetime import datetime
import agro_exception as ae
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 10:
                continue
            if part[9] == 'Ready':
                harvest = convert_date(part[7])
                listing = convert_date(part[8])
                if (harvest - listing).days <= 20:
                    records.append(line)
    return records

def validate_crop_code(crop_code):
    if len(crop_code) != 11:
        raise ae.InvalidCropCodeException(f"Invalid Crop Code: {crop_code}")
    if re.fullmatch(r"^CRP-[A-Z]\d{2}-\d{3}$", crop_code):
        return True
    raise ae.InvalidCropCodeException(f"Invalid Crop Code: {crop_code}")

def validate_agri_id(agri_id):
    if len(agri_id) < 5:
        raise ae.InvalidAgriIdException("Invalid Agri Id")
    if re.fullmatch(r"^AG\d{3,}$", agri_id):
        return True
    raise ae.InvalidAgriIdException("Invalid Agri Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
