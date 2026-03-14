### officer.py
### Entity class for Officer

class Officer:
    def __init__(self, officer_id, officer_name, badge_number,
                 rank, department, joining_date):
        self.__officer_id   = officer_id
        self.__officer_name = officer_name
        self.__badge_number = badge_number
        self.__rank         = rank
        self.__department   = department
        self.__joining_date = joining_date   # datetime.date object

    def get_officer_id(self):
        return self.__officer_id

    def set_officer_id(self, officer_id):
        self.__officer_id = officer_id

    def get_officer_name(self):
        return self.__officer_name

    def set_officer_name(self, officer_name):
        self.__officer_name = officer_name

    def get_badge_number(self):
        return self.__badge_number

    def set_badge_number(self, badge_number):
        self.__badge_number = badge_number

    def get_rank(self):
        return self.__rank

    def set_rank(self, rank):
        self.__rank = rank

    def get_department(self):
        return self.__department

    def set_department(self, department):
        self.__department = department

    def get_joining_date(self):
        return self.__joining_date

    def set_joining_date(self, joining_date):
        self.__joining_date = joining_date
