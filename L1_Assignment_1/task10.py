# ### Task 10 - `Write a function validate_password(password) that ensures the password has:`
# `At least 8 characters`
# `At least one uppercase letter`
# `At least one lowercase letter`
# `At least one digit`
# `Raise WeakPasswordException if the password is weak.`


import json
import re

class WeakPasswordException(Exception):
    pass

def valid_pass(pw):
    pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    if not (re.match(pattern,pw)):
        raise WeakPasswordException(f"Invalid Password: {pw}")
    return True

def main():
    with open("validation_test_data.json","r") as f:
        lst=json.load(f)
        for pw in lst["passwords"]:
            try:
                if valid_pass(pw):
                    print(f"{pw} is valid")
            except WeakPasswordException as e:
                print(e)        
    return
            
if __name__=="__main__":
    main()