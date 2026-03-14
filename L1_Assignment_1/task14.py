### Task 14 - `Write a function convert_ddmmyyyy(str_date) 
# that takes a string in the format "DD/MM/YYYY" 
# and returns a datetime.date object.`



from datetime import datetime,date,time,timedelta
import json

def convert_ddmmyyyy(s):
    return datetime.strptime(s,"%d/%m/%Y")

def main():
    with open("date_task_samples.json","r") as f:
        dt=json.load(f)
        for s in dt["convert_ddmmyyyy_inputs"]:
            d=convert_ddmmyyyy(s)
            print(d.strftime("%Y-%m-%d"))

if __name__=="__main__":
    main()