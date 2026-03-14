from datetime import datetime,date,timedelta

def convert(s):
    return datetime.strptime(s,"%d-%m-%Y")

def main():
    d1=input("Enter date 1 (DD-MM-YYYY ): ")
    d2=input("Enter date 2 (DD-MM-YYYY ): ")
    
    d1=convert(d1)
    d2=convert(d2)
    no_of_day=abs((d1-d2).days)
    print(no_of_day)

if __name__=="__main__":
    main()