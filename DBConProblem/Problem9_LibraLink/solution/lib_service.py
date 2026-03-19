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
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE BookIssue")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_book_code(part[1])
                ut.validate_issue_id(part[0])
                id_ = ut.convert_date(part[4]); dd = ut.convert_date(part[5]); rd = ut.convert_date(part[6])
                obj = bi.BookIssue(part[0], part[1], part[2], part[3], id_, dd, rd, part[7])
                fine = obj.calculate_fine()
                self.add_issue_details(obj)
                self.__fine_dict[obj.get_issue_id()] = fine
            except le.InvalidBookCodeException as e: print(e.get_message())
            except le.InvalidIssueIdException as e: print(e.get_message())
        return None

    def add_issue_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into BookIssue values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
            cur.execute(q, [obj.get_issue_id(), obj.get_book_code(), obj.get_member_name(),
                            obj.get_genre(), obj.get_issue_date(), obj.get_due_date(),
                            obj.get_return_date(), obj.get_member_type(),
                            obj.get_overdue_days(), obj.get_fine_per_day(), obj.get_total_fine()])
            conn.commit()
        return None

    def find_top3_books(self):
        with conn.cursor() as cur:
            cur.execute("select * from BookIssue")
            freq = {}
            for row in cur.fetchall(): freq[row[1]] = freq.get(row[1], 0) + 1
            sorted_f = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
            res = {}; i = prev = 0
            for k, v in sorted_f.items():
                if v != prev: prev = v; i += 1
                if i > 3: break
                res[k] = v
            return res

    def search_issue(self, issue_id):
        with conn.cursor() as cur:
            cur.execute("select * from BookIssue where issue_id=:1", (issue_id,))
            row = cur.fetchone()
            if row is None: return None
            obj = bi.BookIssue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            obj.set_overdue_days(row[8]); obj.set_fine_per_day(row[9]); obj.set_total_fine(row[10])
            return obj

    def find_overdue_issues(self, start_date, end_date):
        with conn.cursor() as cur:
            cur.execute("""select issue_id, overdue_days from BookIssue
                           where overdue_days > 5 and return_date between :1 and :2""",
                        (start_date, end_date))
            return {iid: od for iid, od in cur.fetchall()}

    def update_fine(self, member_type):
        with conn.cursor() as cur:
            cur.execute("""update BookIssue
                           set fine_per_day = fine_per_day * 1.20,
                               total_fine = overdue_days * (fine_per_day * 1.20)
                           where member_type = :1""", (member_type,))
            conn.commit()
            cur.execute("select * from BookIssue where member_type = :1", (member_type,))
            rows = cur.fetchall()
            if not rows: return None
            result = []
            for row in rows:
                obj = bi.BookIssue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                obj.set_overdue_days(row[8]); obj.set_fine_per_day(row[9]); obj.set_total_fine(row[10])
                result.append(obj)
            return result
