### employee_dao.py
### Data Access Object Class — all DB operations for Employee
### Class-based DAO with SELECT operation

import employee as emp
import cx_Oracle
from exceptions import InvalidDepartmentException


class EmployeeDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all employees for a given department
    # ----------------------------------------------------------------
    def retrieve_employees_by_department(self, department):
        cursor = self.__conn.cursor()

        query = """
            SELECT emp_id, emp_name, department, designation,
                   basic_salary, joining_date
            FROM employee
            WHERE LOWER(department) = :1
            ORDER BY emp_id ASC
        """

        cursor.execute(query, (department.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise InvalidDepartmentException(
                "No employees found in the given department.")

        employee_list = []
        for row in rows:
            # Safely handle Oracle datetime vs date
            j_date = row[5].date() if hasattr(row[5], 'date') else row[5]
            obj    = emp.Employee(row[0], row[1], row[2], row[3],
                                  float(row[4]), j_date)
            employee_list.append(obj)

        return employee_list
