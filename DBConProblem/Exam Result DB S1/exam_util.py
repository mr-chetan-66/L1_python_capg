### exam_util.py
### Utility / helper functions for ExamResult — validation, display and calculations

VALID_GRADES = ['O', 'A+', 'A', 'B+', 'B', 'C', 'F']


def is_valid_student_id(student_id):
    # Returns True only if student_id is a positive integer
    return student_id > 0


def is_valid_result_id(result_id):
    # Returns True only if result_id is a positive integer
    return result_id > 0


def display_result(result):
    print("Result ID      :", result.get_result_id())
    print("Student ID     :", result.get_student_id())
    print("Subject        :", result.get_subject())
    print("Exam Date      :", result.get_exam_date())
    print("Marks Obtained :", result.get_marks_obtained(), "/", result.get_max_marks())
    print("Grade          :", result.get_grade())
    print("-" * 40)


def get_result_count(result_list):
    return len(result_list)


def calculate_percentage(result_list):
    # Returns overall percentage: (sum of marks_obtained / sum of max_marks) * 100
    # Returns -1 if list is empty
    if not result_list:
        return -1

    total_obtained = sum(r.get_marks_obtained() for r in result_list)
    total_max      = sum(r.get_max_marks()      for r in result_list)

    return round((total_obtained / total_max) * 100, 2)


def get_pass_fail_summary(result_list):
    # Returns a dict with 'passed' and 'failed' counts
    # A result is considered failed if grade == 'F'
    passed = sum(1 for r in result_list if r.get_grade() != 'F')
    failed = sum(1 for r in result_list if r.get_grade() == 'F')
    return {'passed': passed, 'failed': failed}


def get_performance_remark(percentage):
    # Returns a performance remark string based on percentage
    if percentage >= 90:
        return "Outstanding"
    elif percentage >= 75:
        return "Distinction"
    elif percentage >= 60:
        return "First Class"
    elif percentage >= 50:
        return "Second Class"
    elif percentage >= 35:
        return "Pass"
    else:
        return "Fail"
