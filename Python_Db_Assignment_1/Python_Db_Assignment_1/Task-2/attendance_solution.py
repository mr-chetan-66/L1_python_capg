import attendance_db_setup as dbs
import attendance_entity as ae
import oracledb

class AttendanceRepository:

    def record_attendance(self, attendance_list):
        db=""
        with open("database.properties") as f:
            lines = [
                line.strip().split("=")
                for line in f.readlines()
                if not line.startswith("#") and line.strip()
            ]
            db = {k.strip(): v.strip() for k, v in lines}

        # Connect to Oracle
        inserted=0
        with oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"]) as conn:
            with conn.cursor() as cur:
                query="""
                INSERT INTO attendance(employee_id, att_date, status)
                VALUES (:1,TO_DATE(:2,'YYYY-MM-DD'),:3)
                """
                
                for obj in attendance_list:
                    try:
                        cur.execute(query,(obj.get_employee_id(),obj.get_date(),obj.get_status()))
                        inserted+=1
                    except oracledb.DatabaseError as e:
                            raise
            conn.commit()
        return inserted
                    

# --- Optional quick demo ---
if __name__ == "__main__":
    # Ensure you ran attendance_db_setup.py once before this.
    repo = AttendanceRepository()
    dbs.start()
    
    new_records = [
        ae.Attendance(1, "2024-07-03", "Present"),
        ae.Attendance(2, "2024-07-02", "Present"),
        ae.Attendance(2, "2024-07-03", "Absent"),
        # Duplicate primary key (will be skipped)
        ae.Attendance(1, "2024-07-01", "Present"),
    ]

    count = repo.record_attendance(new_records)
    print(f"Inserted {count} attendance records.")