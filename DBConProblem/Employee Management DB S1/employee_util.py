### employee_util.py
### Utility / helper functions for Employee — validation and display


def is_valid_salary_range(min_salary, max_salary):
    # Returns True only if both salaries are positive and min < max
    if min_salary <= 0 or max_salary <= 0:
        return False
    if min_salary >= max_salary:
        return False
    return True


def display_employee(employee):
    print("Emp ID      :", employee.get_emp_id())
    print("Name        :", employee.get_name())
    print("Designation :", employee.get_designation())
    print("Department  :", employee.get_department())
    print("Salary      :", employee.get_salary())
    print("Joining Date:", employee.get_joining_date())
    print("-" * 35)


def get_result_count(employee_list):
    return len(employee_list)


def calculate_average_salary(employee_list):
    # Returns average salary of all employees in the list
    # Returns 0 if list is empty
    if not employee_list:
        return 0
    total = sum(e.get_salary() for e in employee_list)
    return round(total / len(employee_list), 2)
