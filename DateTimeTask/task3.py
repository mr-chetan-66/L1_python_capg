from datetime import datetime, date, timedelta

def convert(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def main():
    d = "2026-03-09"
    n = 30
    print("Current Date:", d, "(", convert(d).strftime("%A"), ")")

    d = convert(d)
    d = d + timedelta(days=n)

    print("After 30 Days:", d.strftime("%Y-%m-%d"), "(", d.strftime("%A"), ")")

if __name__ == "__main__":
    main()