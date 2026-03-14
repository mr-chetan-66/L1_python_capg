### Task 16 - `Write a function calculate_age(birthdate_str) 
# that takes a birthdate string in "YYYY-MM-DD"
# format and returns the age in years.`

import json
from datetime import datetime
def calculate_age(bds):
    today=datetime.today().date()
    age=today.year-bds.year
    
    if(today.month,today.day)<(bds.month,bds.day):
        age-=1
        
    return age

def main():
    with open("date_task_samples.json","r") as f:
        lst=json.load(f)
        i=0
        for s in lst["calculate_age_inputs"]:
            d=datetime.strptime(s,"%Y-%m-%d")
            print(f"Age of {i+1} person is {calculate_age(d)}")
            i+=1
            
if __name__=="__main__":
    main()