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
    obj=ss.ScholarshipService()
    record=obj.get_scholarship_details("input.txt")
    obj.add_scholarship_details(record)
    
    sid=input("Enter the Application Id: ")
    try:
        ut.validate_application_id(sid)
        row=obj.search_application(sid)
        if row is None:
            print("No application found with Id")
        else:
            display(row)
    except ex.InvalidApplicationIdException as e:
        print(e.get_message())
    
    cgpa=float(input("Enter the CGPA threshold for merit bonus update: "))
    
    rows=obj.update_merit_bonus(cgpa)
    
    if rows is None:
        print("No record updated")
    else:
        for row in rows:
            display(row)

if __name__ == "__main__":
    main()
