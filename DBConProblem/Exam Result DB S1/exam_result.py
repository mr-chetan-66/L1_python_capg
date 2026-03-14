### exam_result.py
### Entity class for ExamResult

class ExamResult:
    def __init__(self, result_id, student_id, subject, exam_date, marks_obtained, max_marks, grade):
        self.__result_id      = result_id
        self.__student_id     = student_id
        self.__subject        = subject
        self.__exam_date      = exam_date
        self.__marks_obtained = marks_obtained
        self.__max_marks      = max_marks
        self.__grade          = grade

    def get_result_id(self):
        return self.__result_id

    def set_result_id(self, result_id):
        self.__result_id = result_id

    def get_student_id(self):
        return self.__student_id

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def get_subject(self):
        return self.__subject

    def set_subject(self, subject):
        self.__subject = subject

    def get_exam_date(self):
        return self.__exam_date

    def set_exam_date(self, exam_date):
        self.__exam_date = exam_date

    def get_marks_obtained(self):
        return self.__marks_obtained

    def set_marks_obtained(self, marks_obtained):
        self.__marks_obtained = marks_obtained

    def get_max_marks(self):
        return self.__max_marks

    def set_max_marks(self, max_marks):
        self.__max_marks = max_marks

    def get_grade(self):
        return self.__grade

    def set_grade(self, grade):
        self.__grade = grade
