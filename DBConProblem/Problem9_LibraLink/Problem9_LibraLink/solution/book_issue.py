from datetime import date

class BookIssue:
    def __init__(self, issue_id, book_code, member_name, genre,
                 issue_date, due_date, return_date, member_type):
        self.__issue_id = issue_id; self.__book_code = book_code
        self.__member_name = member_name; self.__genre = genre
        self.__issue_date = issue_date; self.__due_date = due_date
        self.__return_date = return_date; self.__member_type = member_type
        self.__overdue_days = 0; self.__fine_per_day = 0.0; self.__total_fine = 0.0

    def get_issue_id(self): return self.__issue_id
    def get_book_code(self): return self.__book_code
    def get_member_name(self): return self.__member_name
    def get_genre(self): return self.__genre
    def get_issue_date(self): return self.__issue_date
    def get_due_date(self): return self.__due_date
    def get_return_date(self): return self.__return_date
    def get_member_type(self): return self.__member_type
    def get_overdue_days(self): return self.__overdue_days
    def get_fine_per_day(self): return self.__fine_per_day
    def get_total_fine(self): return self.__total_fine
    def set_issue_id(self, v): self.__issue_id = v
    def set_book_code(self, v): self.__book_code = v
    def set_member_name(self, v): self.__member_name = v
    def set_genre(self, v): self.__genre = v
    def set_issue_date(self, v): self.__issue_date = v
    def set_due_date(self, v): self.__due_date = v
    def set_return_date(self, v): self.__return_date = v
    def set_member_type(self, v): self.__member_type = v
    def set_overdue_days(self, v): self.__overdue_days = v
    def set_fine_per_day(self, v): self.__fine_per_day = v
    def set_total_fine(self, v): self.__total_fine = v

    def calculate_fine(self):
        od = (self.__return_date - self.__due_date).days
        if od <= 0:
            self.__overdue_days = 0; self.__fine_per_day = 0.0; self.__total_fine = 0.0
            return 0.0
        fpd = 5.0 if self.__member_type == "Premium" else 10.0
        total = od * fpd
        self.__overdue_days = od; self.__fine_per_day = fpd; self.__total_fine = total
        return total
