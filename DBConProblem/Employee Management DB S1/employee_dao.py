### employee_dao.py
### Data Access Object — contains all DB query functions for Employee

import employee as emp


def retrieve_employees_by_salary_range(min_salary, max_salary, conn):
    cursor = conn.cursor()

    query = """
        SELECT emp_id, name, designation, department, salary, joining_date
        FROM employee
        WHERE salary BETWEEN :1 AND :2
        ORDER BY salary ASC
    """

    cursor.execute(query, (min_salary, max_salary))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    employee_list = []
    for row in rows:
        emp_obj = emp.Employee(row[0], row[1], row[2], row[3], row[4], row[5])
        employee_list.append(emp_obj)

    return employee_list
