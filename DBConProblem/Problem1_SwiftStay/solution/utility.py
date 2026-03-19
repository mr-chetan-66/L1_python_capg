from datetime import datetime
import hotel_exception as he
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 9:
                continue
            status = part[7]
            if status == 'Confirmed':
                check_in = convert_date(part[5])
                booking_date = convert_date(part[8])
                if (check_in - booking_date).days <= 60:
                    records.append(line)
    return records


def validate_room_number(room_number):
    if len(room_number) != 10:
        raise he.InvalidRoomNumberException(f"Invalid Room Number: {room_number}")
    if re.fullmatch(r"^RMH\d{3}.{3}[A-Z]$", room_number):
        return True
    else:
        raise he.InvalidRoomNumberException(f"Invalid Room Number: {room_number}")


def validate_booking_id(booking_id):
    if len(booking_id) < 5:
        raise he.InvalidBookingIdException("Invalid Booking Id")
    if re.fullmatch(r"^BK\d{3,}$", booking_id):
        return True
    else:
        raise he.InvalidBookingIdException("Invalid Booking Id")


def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
