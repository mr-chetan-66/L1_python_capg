from datetime import datetime
import freight_exception as fe
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 9:
                continue
            status = part[7]
            if status == 'Dispatched':
                dispatch_date = convert_date(part[5])
                booking_date = convert_date(part[8])
                if (dispatch_date - booking_date).days <= 30:
                    records.append(line)
    return records

def validate_freight_id(freight_id):
    if len(freight_id) != 10:
        raise fe.InvalidFreightIdException(f"Invalid Freight Id: {freight_id}")
    if re.fullmatch(r"^FRT-\d{4}-[A-Z]{2}$", freight_id):
        return True
    else:
        raise fe.InvalidFreightIdException(f"Invalid Freight Id: {freight_id}")

def validate_shipment_id(shipment_id):
    if len(shipment_id) < 5:
        raise fe.InvalidShipmentIdException("Invalid Shipment Id")
    if re.fullmatch(r"^SH\d{3,}$", shipment_id):
        return True
    else:
        raise fe.InvalidShipmentIdException("Invalid Shipment Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
