from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[7]
            units = float(parts[5])
            if status == 'Pending' and units >= 50:
                bd = convert_date(parts[2])
                rd = convert_date(parts[4])
                if (rd - bd).days <= 60:
                    records.append(line)
    return records


def validate_bill_id(bill_id):
    if len(bill_id) < 6:
        raise ex.InvalidBillIdException("Invalid Bill Id")
    if re.fullmatch(r"^ENB\d+$", bill_id):
        return True
    else:
        raise ex.InvalidBillIdException("Invalid Bill Id")


def validate_consumer_type(consumer_type):
    valid_types = ['Residential', 'Commercial', 'Industrial', 'Agricultural']
    if consumer_type in valid_types:
        return True
    else:
        raise ex.InvalidConsumerTypeException("Invalid Consumer Type")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
