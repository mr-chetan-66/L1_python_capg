### student_dao.py
### Data Access Object — contains all DB query functions for Student

import student as st


def retrieve_toppers_by_department(department, conn):
    cursor = conn.cursor()

    query = """
        SELECT student_id, name, department, year, marks
        FROM student
        WHERE LOWER(department) = LOWER(:1)
          AND marks >= 90
        ORDER BY marks DESC
    """

    cursor.execute(query, (department,))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    student_list = []
    for row in rows:
        student_obj = st.Student(row[0], row[1], row[2], row[3], row[4])
        student_list.append(student_obj)

    return student_list
