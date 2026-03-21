from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[7]
            if status == 'Delivered':
                dod = convert_date(parts[2])
                dodl = convert_date(parts[4])
                if (dodl - dod).days <= 60:
                    records.append(line)
    return records


def validate_shipment_id(shipment_id):
    if len(shipment_id) < 4:
        raise ex.InvalidShipmentIdException("Invalid Shipment Id")
    if re.fullmatch(r"^SHP\d+$", shipment_id):
        return True
    else:
        raise ex.InvalidShipmentIdException("Invalid Shipment Id")


def validate_zone(zone):
    valid_zones = ['Zone_A', 'Zone_B', 'Zone_C', 'Zone_D']
    if zone in valid_zones:
        return True
    else:
        raise ex.InvalidZoneException("Invalid Zone")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
