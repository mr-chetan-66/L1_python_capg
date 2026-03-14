### Task 8 - `Write a function validate_phone(phone) that ensures the phone 
# number is exactly 10 digits and starts with 7, 8, or 9. 
# Raise InvalidPhoneNumberException if invalid.`

import json
import re

class InvalidPhoneNumberException(Exception):
    pass

def valid_ph(ph):
    pattern=r'^[789]\d{9}$'
    if not (re.match(pattern,ph)):
        raise InvalidPhoneNumberException(f"Invalid Phone Number: {ph}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for ph in lst["phones"]:
            try:
                if valid_ph(ph):
                    print(f"{ph} is valid")
            except InvalidPhoneNumberException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()