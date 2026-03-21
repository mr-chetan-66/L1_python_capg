# Please do not change the skeleton code given here.
import oracledb

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class TalentService:

    def __init__(self):
        self.__bonus_dict = {}

    def read_data(self, records):
        
        pass

    def add_application_details(self, obj):
        
        pass

    def find_top3_jobs(self):
        
        pass

    def search_application(self, application_id):
        
        pass

    def find_senior_applicants(self, start_date, end_date):
        
        pass

    def update_offered_salary(self, experience_grade):
        
        pass
