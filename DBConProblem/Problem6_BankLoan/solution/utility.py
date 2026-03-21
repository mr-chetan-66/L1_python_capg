from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[8]
            if status == 'Approved':
                doa = convert_date(parts[2])
                dod = convert_date(parts[4])
                if (dod - doa).days <= 30:
                    records.append(line)
    return records


def validate_loan_id(loan_id):
    if len(loan_id) < 5:
        raise ex.InvalidLoanIdException("Invalid Loan Id")
    if re.fullmatch(r"^LN\d+$", loan_id):
        return True
    else:
        raise ex.InvalidLoanIdException("Invalid Loan Id")


def validate_loan_type(loan_type):
    valid_types = ['Home', 'Vehicle', 'Personal', 'Education']
    if loan_type in valid_types:
        return True
    else:
        raise ex.InvalidLoanTypeException("Invalid Loan Type")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
