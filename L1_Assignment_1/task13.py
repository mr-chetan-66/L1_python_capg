# ### Tasks 13–17 – Date Utilities
# - **File:** `date_task_samples.json`

### Task 13 - `Write a function format_date(date_obj) that takes a datetime.
# date object and returns a string in the format "YYYY-MM-DD".`

from datetime import datetime,date,time,timedelta
import json

def format_date(d):
    return d.strftime("%Y-%m-%d")

def main():
    with open("date_task_samples.json","r") as f:
        dt=json.load(f)
        for s in dt["format_date_inputs"]:
            d=datetime.strptime(s,"%Y/%m/%d")
            print(format_date(d))

if __name__=="__main__":
    main()