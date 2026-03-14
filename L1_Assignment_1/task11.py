### Task 11 - `Write a function validate_vehicle_number(number)
# that checks if the number follows the format: KA01AB1234. 
# Raise InvalidVehicleNumberException if invalid.`


import json
import re

class InvalidVehicleNumberException(Exception):
    pass

def valid_vnum(vnum):
    pattern=r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$'
    if not (re.match(pattern,vnum)):
        raise InvalidVehicleNumberException(f"Invalid Vehicle Number: {vnum}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for vnum in lst["vehicle_numbers"]:
            try:
                if valid_vnum(vnum):
                    print(f"{vnum} is valid")
            except InvalidVehicleNumberException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()