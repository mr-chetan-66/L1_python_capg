# ### Tasks 7–12 – Validators
# - **File:** `validation_test_data.json`
# - **Purpose:** Contains arrays of test strings for:
# emails, phones, PANs, passwords, vehicle numbers, and booking codes. 
# Includes both valid and invalid examples. Use these to check exception handling for:
#   - `InvalidEmailException
#   - `InvalidPhoneNumberException
#   - `InvalidPANException
#   - `WeakPasswordException
#   - `InvalidVehicleNumberException
#   - `InvalidBookingCodeException

### Task 7 - `Write a function  that checks if 
# the email is in a valid format (e.g., example@domain.com). 
# If not, raise a custom InvalidEmailException.`

import json
import re

class InvalidEmailException(Exception):
    pass

def valid_email(mail):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not (re.match(pattern, mail)):
        raise InvalidEmailException(f"Invalid Email: {mail}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for email in lst["emails"]:
            try:
                if valid_email(email):
                    print(f"{email} is valid")
            except InvalidEmailException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()