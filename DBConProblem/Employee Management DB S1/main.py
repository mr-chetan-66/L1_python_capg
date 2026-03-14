### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import employee_dao as dao
import employee_util as util


def main():
    conn = db.get_connection()

    min_salary = float(input("Enter the minimum salary: "))
    max_salary = float(input("Enter the maximum salary: "))

    if not util.is_valid_salary_range(min_salary, max_salary):
        print("Invalid Salary Range")
        return

    result = dao.retrieve_employees_by_salary_range(min_salary, max_salary, conn)

    if not result:
        print("No employees found")
        return

    print("Total employees found:", util.get_result_count(result))
    print("Average Salary       :", util.calculate_average_salary(result))
    print("-" * 35)

    for employee in result:
        util.display_employee(employee)


if __name__ == '__main__':
    main()
