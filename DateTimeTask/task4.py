from datetime import datetime,date,timedelta

def convert(s):
    return datetime.strptime(s,"%Y-%m-%d").date()

def main():
    dates = ["2026-03-01", "2026-03-09", "2026-03-10", "2026-02-28"]
    start = "2026-03-01"
    end = "2026-03-10"

    s=convert(start)
    e=convert(end)
    res=[d for d in dates if s<=convert(d)<=e]
            
    for d in res:
        print(d)
        
if __name__=="__main__":
    main()