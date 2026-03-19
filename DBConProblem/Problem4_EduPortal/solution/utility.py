from datetime import datetime
import edu_exception as ee
import re

def read_file(file):
    records = []
    with open(file) as f:
        for line in f:
            part = line.strip().split(",")
            if len(part) < 9:
                continue
            if part[8] == 'Active':
                start = convert_date(part[5])
                reg = convert_date(part[6])
                if (start - reg).days <= 20:
                    records.append(line)
    return records

def validate_course_code(course_code):
    if len(course_code) != 11:
        raise ee.InvalidCourseCodeException(f"Invalid Course Code: {course_code}")
    if re.fullmatch(r"^CRS-[A-Z]{2}-\d{4}$", course_code):
        return True
    raise ee.InvalidCourseCodeException(f"Invalid Course Code: {course_code}")

def validate_enrollment_id(enrollment_id):
    if len(enrollment_id) < 5:
        raise ee.InvalidEnrollmentIdException("Invalid Enrollment Id")
    if re.fullmatch(r"^EN\d{3,}$", enrollment_id):
        return True
    raise ee.InvalidEnrollmentIdException("Invalid Enrollment Id")

def convert_date(str_date):
    return datetime.strptime(str_date.strip(), "%d/%m/%Y").date()
