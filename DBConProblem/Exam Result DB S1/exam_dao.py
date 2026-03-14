### exam_dao.py
### Data Access Object Class — all DB operations for ExamResult
### Class-based DAO that holds the connection as an instance variable

import exam_result as er


class ExamDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all results for a student, newest first
    # ----------------------------------------------------------------
    def retrieve_results_by_student(self, student_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT result_id, student_id, subject, exam_date,
                   marks_obtained, max_marks, grade
            FROM exam_result
            WHERE student_id = :1
            ORDER BY exam_date DESC
        """

        cursor.execute(query, (student_id,))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return []

        result_list = []
        for row in rows:
            result_obj = er.ExamResult(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            result_list.append(result_obj)

        return result_list

    # ----------------------------------------------------------------
    # SELECT — retrieve a single result by result_id
    # ----------------------------------------------------------------
    def retrieve_result_by_id(self, result_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT result_id, student_id, subject, exam_date,
                   marks_obtained, max_marks, grade
            FROM exam_result
            WHERE result_id = :1
        """

        cursor.execute(query, (result_id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return er.ExamResult(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    # ----------------------------------------------------------------
    # DELETE — remove a result record by result_id
    # ----------------------------------------------------------------
    def delete_result(self, result_id):
        # Check if the result exists first
        result = self.retrieve_result_by_id(result_id)

        if result is None:
            return "Result Not Found"

        cursor = self.__conn.cursor()

        delete_query = """
            DELETE FROM exam_result
            WHERE result_id = :1
        """

        cursor.execute(delete_query, (result_id,))
        self.__conn.commit()
        cursor.close()

        return "Result Deleted Successfully"

    # ----------------------------------------------------------------
    # SELECT — retrieve top scoring result for a student
    # ----------------------------------------------------------------
    def retrieve_best_result(self, student_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT result_id, student_id, subject, exam_date,
                   marks_obtained, max_marks, grade
            FROM exam_result
            WHERE student_id = :1
              AND marks_obtained = (
                    SELECT MAX(marks_obtained)
                    FROM exam_result
                    WHERE student_id = :2
                  )
        """

        cursor.execute(query, (student_id, student_id))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return er.ExamResult(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
