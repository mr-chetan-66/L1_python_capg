from datetime import datetime
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

def convert(s: str) -> datetime:
    return datetime.strptime(s, "%d-%m-%Y")

def main():
    d1 = convert(input("Enter date 1 (DD-MM-YYYY): "))
    d2 = convert(input("Enter date 2 (DD-MM-YYYY): "))

    rd = relativedelta(max(d1, d2), min(d1, d2))
    # You can get total months as:
    total_months = rd.years * 12 + rd.months
    print("Whole calendar months between (ignoring leftover days):", total_months)
    print("Breakdown -> years:", rd.years, "months:", rd.months, "days:", rd.days)

if __name__ == "__main__":
    main()