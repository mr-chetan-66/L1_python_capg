# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import scholarship_service as ss
import utility as ut


def display(o):
    print(f"\nApplication Id: {o.get_application_id()}")
    print(f"Student Id: {o.get_student_id()}")
    print(f"Course Type: {o.get_course_type()}")
    print(f"Date of Enrollment: {o.get_date_of_enrollment()} 00:00:00")
    print(f"CGPA: {o.get_cgpa()}")
    print(f"Annual Family Income: {o.get_annual_family_income()}")
    print(f"Category: {o.get_category()}")
    print(f"Base Scholarship: {o.get_base_scholarship()}")
    print(f"Merit Bonus: {o.get_merit_bonus()}")
    print(f"Income Waiver: {o.get_income_waiver()}")
    print(f"Total Scholarship: {o.get_total_scholarship()}")


def main():
    # Step 1: Load and insert all valid scholarship records
    # Write your code here

    # Step 2: Accept application_id from user, validate, search and display.
    # Invalid id -> print exception message
    # Not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept cgpa_threshold from user (float), call update_merit_bonus(),
    # display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
