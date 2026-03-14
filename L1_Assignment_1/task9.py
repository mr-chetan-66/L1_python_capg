### Task 9 - `Write a function validate_pan(pan) that checks 
# if the PAN number follows the format: 5 uppercase letters, 4 digits,
# and 1 uppercase letter (e.g., ABCDE1234F). Raise InvalidPANException if invalid.`


import json
import re

class InvalidPANException(Exception):
    pass

def valid_pan(pan):
    pattern=r'^[A-Z]{5}\d{4}[A-Z]$'
    if not (re.match(pattern,pan)):
        raise InvalidPANException(f"Invalid Pan: {pan}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for pan in lst["pans"]:
            try:
                if valid_pan(pan):
                    print(f"{pan} is valid")
            except InvalidPANException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()