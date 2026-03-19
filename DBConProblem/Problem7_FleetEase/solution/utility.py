from datetime import datetime
import fleet_exception as fe
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 8: continue
            if part[7] == 'Approved':
                sd = convert_date(part[5])
                bd = convert_date(part[6])
                if (sd - bd).days <= 10:
                    records.append(line)
    return records

def validate_vehicle_id(vehicle_id):
    if len(vehicle_id) != 11:
        raise fe.InvalidVehicleIdException(f"Invalid Vehicle Id: {vehicle_id}")
    if re.fullmatch(r"^VEH-[A-Z]{3}-\d{3}$", vehicle_id):
        return True
    raise fe.InvalidVehicleIdException(f"Invalid Vehicle Id: {vehicle_id}")

def validate_service_id(service_id):
    if len(service_id) < 5:
        raise fe.InvalidServiceIdException("Invalid Service Id")
    if re.fullmatch(r"^VS\d{3,}$", service_id):
        return True
    raise fe.InvalidServiceIdException("Invalid Service Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
