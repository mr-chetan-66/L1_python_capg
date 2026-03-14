### Task 17 - `Write a function reformat_date(str_date) 
# that takes a date string in "YYYY-MM-DD" format and returns 
# it in "Month Day, Year" format (e.g., "2025-06-13" → "June 13, 2025").`
import json
from datetime import datetime

def reformat_date(d):
    return d.strftime("%B %d, %Y") # %B-full month name %b- 3 letter month name
    
def main():
    with open("date_task_samples.json","r") as f:
        lst=json.load(f)
        
        for s in lst["reformat_date_inputs"]:
            d=datetime.strptime(s,"%Y-%m-%d")
            print(f"{s} -> {reformat_date(d)}")

if __name__=="__main__":
    main()