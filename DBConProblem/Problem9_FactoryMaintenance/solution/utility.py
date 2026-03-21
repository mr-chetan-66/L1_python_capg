from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[7]
            operating_hours = int(parts[5])
            if status == 'Scheduled' and operating_hours >= 100:
                dls = convert_date(parts[2])
                dns = convert_date(parts[4])
                if (dns - dls).days <= 365:
                    records.append(line)
    return records


def validate_maintenance_id(maintenance_id):
    if len(maintenance_id) < 6:
        raise ex.InvalidMaintenanceIdException("Invalid Maintenance Id")
    if re.fullmatch(r"^MNT\d+$", maintenance_id):
        return True
    else:
        raise ex.InvalidMaintenanceIdException("Invalid Maintenance Id")


def validate_equipment_type(equipment_type):
    valid_types = ['CNC', 'Hydraulic', 'Conveyor', 'Electrical']
    if equipment_type in valid_types:
        return True
    else:
        raise ex.InvalidEquipmentTypeException("Invalid Equipment Type")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
