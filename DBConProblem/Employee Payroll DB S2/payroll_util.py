### payroll_util.py
### Utility / helper functions for Payroll — salary calculation, experience, display, file export

from datetime import date
from exceptions import InsufficientExperienceException


# ----------------------------------------------------------------
# CALCULATION — compute all salary components from basic salary
# ----------------------------------------------------------------
def calculate_net_salary(basic_salary):
    # Allowances
    hra = round(basic_salary * 0.20, 2)
    da  = round(basic_salary * 0.15, 2)
    ta  = round(basic_salary * 0.10, 2)

    # Deductions
    pf  = round(basic_salary * 0.12, 2)
    # Tax is 10% of basic only if basic_salary > 30000
    tax = round(basic_salary * 0.10, 2) if basic_salary > 30000 else 0.0

    gross_salary = round(basic_salary + hra + da + ta, 2)
    net_salary   = round(gross_salary - pf - tax, 2)

    return {
        'hra'          : hra,
        'da'           : da,
        'ta'           : ta,
        'pf'           : pf,
        'tax'          : tax,
        'gross_salary' : gross_salary,
        'net_salary'   : net_salary
    }


# ----------------------------------------------------------------
# CALCULATION — number of complete years from joining date to today
# ----------------------------------------------------------------
def calculate_years_of_experience(joining_date):
    today = date.today()
    years = today.year - joining_date.year

    # Subtract one year if the work anniversary hasn't occurred yet this year
    if (today.month, today.day) < (joining_date.month, joining_date.day):
        years -= 1

    if years < 1:
        raise InsufficientExperienceException(
            "Employee has less than 1 year of experience.")

    return years


# ----------------------------------------------------------------
# DISPLAY — print full payroll details for each employee to console
# ----------------------------------------------------------------
def display_payroll(department, employee_list):
    print(f"\nEmployee Payroll Details - {department}")
    print("=" * 45)

    for e in employee_list:
        salary_info = calculate_net_salary(e.get_basic_salary())

        try:
            exp         = calculate_years_of_experience(e.get_joining_date())
            exp_display = f"{exp} year(s)"
        except InsufficientExperienceException as ex:
            exp_display = str(ex)

        print(f"Emp ID     : {e.get_emp_id()}")
        print(f"Name       : {e.get_emp_name()}")
        print(f"Designation: {e.get_designation()}")
        print(f"Basic      : {e.get_basic_salary()}")
        print(f"HRA        : {salary_info['hra']}")
        print(f"DA         : {salary_info['da']}")
        print(f"TA         : {salary_info['ta']}")
        print(f"Gross      : {salary_info['gross_salary']}")
        print(f"PF         : {salary_info['pf']}")
        print(f"Tax        : {salary_info['tax']}")
        print(f"Net Salary : {salary_info['net_salary']}")
        print(f"Experience : {exp_display}")
        print("-" * 45)


# ----------------------------------------------------------------
# FILE WRITE — export payroll report for all employees to text file
# ----------------------------------------------------------------
def export_payroll_report(employee_list, filename):
    try:
        with open(filename, 'w') as f:
            f.write("Payroll Report\n")
            f.write("=" * 45 + "\n")

            for e in employee_list:
                salary_info = calculate_net_salary(e.get_basic_salary())

                try:
                    exp         = calculate_years_of_experience(e.get_joining_date())
                    exp_display = f"{exp} year(s)"
                except InsufficientExperienceException as ex:
                    exp_display = str(ex)

                f.write(f"Emp ID    : {e.get_emp_id()}\n")
                f.write(f"Name      : {e.get_emp_name()}\n")
                f.write(f"Department: {e.get_department()}\n")
                f.write(f"Basic     : {e.get_basic_salary()}\n")
                f.write(f"Gross     : {salary_info['gross_salary']}\n")
                f.write(f"Net       : {salary_info['net_salary']}\n")
                f.write(f"Experience: {exp_display}\n")
                f.write("-" * 45 + "\n")

    except IOError as e:
        raise IOError(f"Failed to write file: {e}")
