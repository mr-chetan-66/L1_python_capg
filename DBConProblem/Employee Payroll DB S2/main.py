### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import employee_dao as dao_module
import payroll_util as util
from exceptions import InvalidDepartmentException


def main():
    conn         = db.get_connection()
    employee_dao = dao_module.EmployeeDao(conn)

    print("=" * 45)
    print("      EMPLOYEE PAYROLL MANAGEMENT SYSTEM")
    print("=" * 45)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve all employees by department and display payroll
    # ----------------------------------------------------------------
    print("\n--- EMPLOYEE PAYROLL DETAILS ---")

    department    = input("Enter Department : ")
    employee_list = employee_dao.retrieve_employees_by_department(department)

    util.display_payroll(department, employee_list)

    # ----------------------------------------------------------------
    # STEP 2 — Export payroll report to text file
    # ----------------------------------------------------------------
    print("\n--- EXPORT PAYROLL REPORT ---")

    filename = input("Enter Filename to Export Report : ")

    util.export_payroll_report(employee_list, filename)
    print(f"Payroll report exported successfully to {filename}")


if __name__ == '__main__':
    try:
        main()
    except InvalidDepartmentException as e:
        print(e)
    except ValueError:
        print("Invalid input. Please check the entered values.")
