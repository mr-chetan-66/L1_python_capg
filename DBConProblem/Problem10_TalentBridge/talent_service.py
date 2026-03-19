# Please do not change the skeleton code given here.
import utility as ut
import job_application as ja
import oracledb
import talent_exception as te

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class TalentService:

    def __init__(self):
        self.__bonus_dict = {}

    def read_data(self, records):
        # For each line: validate job_code and application_id, convert dates,
        # create JobApplication, call calculate_offered_salary(),
        # store bonus in self.__bonus_dict, call add_application_details().
        # Truncate JobApplication table at start. Return None.
        pass

    def add_application_details(self, obj):
        # Insert into 'JobApplication' table.
        # Column order: application_id, job_code, applicant_name, experience_grade,
        #               years_exp, application_date, closing_date, job_title,
        #               base_salary, experience_bonus, offered_salary
        # Return None.
        pass

    def find_top3_jobs(self):
        # Count appearances of each job_code. Return top 3 distinct counts, ties included.
        pass

    def search_application(self, application_id):
        # Return fully populated JobApplication object or None.
        pass

    def find_senior_applicants(self, start_date, end_date):
        # Find applications where years_exp > 7 and application_date between start and end.
        # Return {application_id: years_exp}. Return empty dict if none.
        pass

    def update_offered_salary(self, experience_grade):
        # UPDATE: offered_salary = offered_salary * 1.10
        #         experience_bonus = experience_bonus * 1.10
        # After update SELECT all with that experience_grade.
        # Return list of JobApplication objects or None.
        pass
