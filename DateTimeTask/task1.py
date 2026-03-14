from datetime import datetime,date,timedelta

def convert(s):
    return datetime.strptime(s,"%d-%m-%Y")
def main():
    s="09-03-2026"
    print("Before: "+s)
    d=convert(s)
    print("After: "+d.strftime("%Y/%m/%d"))

if __name__=="__main__":
    main()