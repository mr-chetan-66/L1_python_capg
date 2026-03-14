### student_util.py
### Utility / helper functions for Student — validation and display

VALID_DEPARTMENTS = ['computer science', 'electronics', 'mechanical', 'civil', 'information technology']


def is_valid_department(department):
    return department.lower() in VALID_DEPARTMENTS


def display_student(student):
    print("Student ID  :", student.get_student_id())
    print("Name        :", student.get_name())
    print("Year        :", student.get_year())
    print("Marks       :", student.get_marks())
    print("-" * 30)


def get_result_count(student_list):
    return len(student_list)
