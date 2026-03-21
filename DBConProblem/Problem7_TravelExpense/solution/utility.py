from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[7]
            if status == 'Approved':
                dot = convert_date(parts[2])
                dor = convert_date(parts[4])
                if (dor - dot).days <= 45:
                    records.append(line)
    return records


def validate_expense_id(expense_id):
    if len(expense_id) < 5:
        raise ex.InvalidExpenseIdException("Invalid Expense Id")
    if re.fullmatch(r"^EXP\d+$", expense_id):
        return True
    else:
        raise ex.InvalidExpenseIdException("Invalid Expense Id")


def validate_city_tier(city_tier):
    valid_tiers = ['Tier1', 'Tier2', 'Tier3']
    if city_tier in valid_tiers:
        return True
    else:
        raise ex.InvalidCityTierException("Invalid City Tier")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
