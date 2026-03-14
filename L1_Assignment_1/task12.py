### Task 12 - `Write a function validate_booking_code(code) that
# checks if the code starts with BOOK followed by exactly 4 digits. 
# Raise InvalidBookingCodeException if invalid.`


import json
import re

class InvalidBookingCodeException(Exception):
    pass

def validate_booking_code(code):
    pattern=r'^BOOK[0-9]{4}$'
    if not (re.match(pattern,code)):
        raise InvalidBookingCodeException(f"Invalid Booking Code: {code}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for code in lst["booking_codes"]:
            try:
                if validate_booking_code(code):
                    print(f"{code} is valid")
            except InvalidBookingCodeException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()