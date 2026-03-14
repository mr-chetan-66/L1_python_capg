### crime_record.py
### Entity class for CrimeRecord

class CrimeRecord:
    def __init__(self, record_id, case_number, crime_type, location,
                 reported_date, status, officer_id, suspect_name):
        self.__record_id     = record_id
        self.__case_number   = case_number
        self.__crime_type    = crime_type
        self.__location      = location
        self.__reported_date = reported_date   # datetime.date object
        self.__status        = status          # 'Open', 'Under Investigation', 'Closed'
        self.__officer_id    = officer_id      # int (foreign key to officer table)
        self.__suspect_name  = suspect_name    # str ('Unknown' if not identified)

    def get_record_id(self):
        return self.__record_id

    def set_record_id(self, record_id):
        self.__record_id = record_id

    def get_case_number(self):
        return self.__case_number

    def set_case_number(self, case_number):
        self.__case_number = case_number

    def get_crime_type(self):
        return self.__crime_type

    def set_crime_type(self, crime_type):
        self.__crime_type = crime_type

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_reported_date(self):
        return self.__reported_date

    def set_reported_date(self, reported_date):
        self.__reported_date = reported_date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_officer_id(self):
        return self.__officer_id

    def set_officer_id(self, officer_id):
        self.__officer_id = officer_id

    def get_suspect_name(self):
        return self.__suspect_name

    def set_suspect_name(self, suspect_name):
        self.__suspect_name = suspect_name
