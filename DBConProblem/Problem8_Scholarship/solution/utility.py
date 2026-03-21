from datetime import date
import exception as ex
import re


def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(",")
            status = parts[8]
            cgpa   = float(parts[5])
            if status == 'Eligible' and cgpa >= 6.0:
                doa = convert_date(parts[2])
                doe = convert_date(parts[4])
                if (doa - doe).days <= 120:
                    records.append(line)
    return records


def validate_application_id(application_id):
    if len(application_id) < 6:
        raise ex.InvalidApplicationIdException("Invalid Application Id")
    if re.fullmatch(r"^SCH\d+$", application_id):
        return True
    else:
        raise ex.InvalidApplicationIdException("Invalid Application Id")


def validate_course_type(course_type):
    valid_types = ['UG', 'PG', 'Diploma', 'PhD']
    if course_type in valid_types:
        return True
    else:
        raise ex.InvalidCourseTypeException("Invalid Course Type")


def convert_date(str_date):
    y, m, d = map(int, str_date.split("-"))
    return date(y, m, d)
