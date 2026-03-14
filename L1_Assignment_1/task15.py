### Task 15 - `Write a function is_valid_date(str_date)
# that checks if a string is a valid date in the format "YYYY-MM-DD". 
# Return True if valid, otherwise False.`

from datetime import datetime,date,time,timedelta
import json

def is_valid_date(s):
    try:
        datetime.strptime(s,"%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def main():
    with open("date_task_samples.json","r") as f:
        dt=json.load(f)
        for s in dt["is_valid_date_inputs"]:
            if is_valid_date(s):
                print(s+" is valid date")
            else:
                print("Invalid date: "+s)

if __name__=="__main__":
    main()