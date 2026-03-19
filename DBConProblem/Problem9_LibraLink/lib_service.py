# Please do not change the skeleton code given here.
import utility as ut
import book_issue as bi
import oracledb
import lib_exception as le

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class LibraService:

    def __init__(self):
        self.__fine_dict = {}

    def read_data(self, records):
        # For each line: validate book_code and issue_id, convert dates,
        # create BookIssue, call calculate_fine(), store fine in self.__fine_dict,
        # call add_issue_details(). Truncate BookIssue table at start. Return None.
        pass

    def add_issue_details(self, obj):
        # Insert into 'BookIssue' table.
        # Column order: issue_id, book_code, member_name, genre, issue_date,
        #               due_date, return_date, member_type,
        #               overdue_days, fine_per_day, total_fine
        # Return None.
        pass

    def find_top3_books(self):
        # Count appearances of each book_code. Return top 3 distinct counts, ties included.
        pass

    def search_issue(self, issue_id):
        # Return fully populated BookIssue object or None.
        pass

    def find_overdue_issues(self, start_date, end_date):
        # Find issues where overdue_days > 5 and return_date between start and end.
        # Return {issue_id: overdue_days}. Return empty dict if none.
        pass

    def update_fine(self, member_type):
        # UPDATE: fine_per_day = fine_per_day * 1.20
        #         total_fine = overdue_days * (fine_per_day * 1.20)
        # After update SELECT all with that member_type.
        # Return list of BookIssue objects or None.
        pass
