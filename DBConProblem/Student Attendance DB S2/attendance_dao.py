### attendance_dao.py
### Data Access Object Class — all DB operations for StudentAttendance
### Class-based DAO with SELECT and aggregation operations

import student_attendance as sa
import cx_Oracle


# Custom Exception — defined here as it is raised inside the DAO
class InvalidDepartmentException(Exception):
    pass


class AttendanceDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all attendance records for a department
    #          between from_date and to_date (inclusive)
    # ----------------------------------------------------------------
    def retrieve_attendance_by_date_range(self, department, from_date, to_date):
        cursor = self.__conn.cursor()

        query = """
            SELECT attendance_id, student_id, student_name, department,
                   attendance_date, status
            FROM attendance
            WHERE LOWER(department) = :1
              AND attendance_date BETWEEN :2 AND :3
            ORDER BY attendance_date ASC
        """

        cursor.execute(query, (department.lower(), from_date, to_date))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise InvalidDepartmentException(
                "No records found for the given department and date range."
            )

        attendance_list = []
        for row in rows:
            obj = sa.StudentAttendance(row[0], row[1], row[2],
                                       row[3], row[4], row[5])
            attendance_list.append(obj)

        return attendance_list

    # ----------------------------------------------------------------
    # SELECT — calculate attendance percentage for a student
    #          Formula: (Total Present / Total Records) * 100
    # ----------------------------------------------------------------
    def calculate_attendance_percentage(self, student_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT COUNT(*),
                   SUM(CASE WHEN LOWER(status) = 'present' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE student_id = :1
        """

        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        cursor.close()

        total   = row[0]
        present = row[1] if row[1] is not None else 0

        if total == 0:
            return -1

        return round((present / total) * 100, 2)
