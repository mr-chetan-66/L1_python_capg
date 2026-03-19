from datetime import datetime
import lib_exception as le
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 8: continue
            due = convert_date(part[5]); ret = convert_date(part[6])
            if (ret - due).days <= 30:
                records.append(line)
    return records

def validate_book_code(book_code):
    if len(book_code) != 11:
        raise le.InvalidBookCodeException(f"Invalid Book Code: {book_code}")
    if re.fullmatch(r"^BK-[A-Z]{3}-\d{4}$", book_code): return True
    raise le.InvalidBookCodeException(f"Invalid Book Code: {book_code}")

def validate_issue_id(issue_id):
    if len(issue_id) < 5:
        raise le.InvalidIssueIdException("Invalid Issue Id")
    if re.fullmatch(r"^LB\d{3,}$", issue_id): return True
    raise le.InvalidIssueIdException("Invalid Issue Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
