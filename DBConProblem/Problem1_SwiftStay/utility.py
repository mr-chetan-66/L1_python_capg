# Please do not change the skeleton code given here.
# Write your code only in the provided places alone
from datetime import datetime
import hotel_exception as he
import re

def read_file(file):
    records=[]
    with open(file) as f:
        for line in f:
            part=line.strip().split(",")
            if part[7]=='Confirmed':
                dob=convert_date(part[8])
                doc=convert_date(part[5])
                if ((doc-dob).days)<=60:
                    records.append(line)
                    
    return records        

def validate_room_number(room_number):
    if re.fullmatch(r"^RMH\d{3}.{3}[A-Z]$",room_number):
        return True
    else:
        raise he.InvalidRoomNumberException(f"Invalid Room Number: {room_number}")

def validate_booking_id(booking_id):
    if len(booking_id)<5:
        raise he.InvalidBookingIdException("Invalid Booking Id")
    if re.fullmatch(r"^BK\d{3,}$",booking_id):
        return True
    else:
        raise he.InvalidBookingIdException("Invalid Booking Id")

def convert_date(str_date):
     return datetime.strptime(str_date,"%d/%m/%Y").date()
