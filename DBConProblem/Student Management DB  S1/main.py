### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import student_dao as dao
import student_util as util


def main():
    conn = db.get_connection()

    department = input("Enter the department: ")

    if not util.is_valid_department(department):
        print("Invalid Department")
        return

    result = dao.retrieve_toppers_by_department(department, conn)

    if not result:
        print("No toppers found")
        return

    print("Total toppers found:", util.get_result_count(result))
    print("-" * 30)

    for student in result:
        util.display_student(student)


if __name__ == '__main__':
    main()
