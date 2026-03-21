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
    svc = ss.ScholarshipService()
    records = svc.get_scholarship_details("input.txt")
    svc.add_scholarship_details(records)

    application_id = input("Enter the Application Id: ")
    try:
        ut.validate_application_id(application_id)
        result = svc.search_application(application_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidApplicationIdException as e:
        print(e.get_message())

    cgpa_threshold = float(input("\n\nEnter the CGPA threshold for merit bonus update: "))
    updated = svc.update_merit_bonus(cgpa_threshold)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
