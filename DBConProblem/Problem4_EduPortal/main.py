# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import utility as ut
import edu_service as es
import edu_exception as ee


def display(obj):
    print(f"\nEnrollment Id: {obj.get_enrollment_id()}")
    print(f"Student Name: {obj.get_student_name()}")
    print(f"Course Code: {obj.get_course_code()}")
    print(f"Course Name: {obj.get_course_name()}")
    print(f"Grade Level: {obj.get_grade_level()}")
    print(f"Start Date: {obj.get_start_date()} 00:00:00")
    print(f"Duration (days): {obj.get_duration_days()}")
    print(f"Base Fee: {obj.get_base_fee()}")
    print(f"Scholarship Amount: {obj.get_scholarship_amount()}")
    print(f"Payable Fee: {obj.get_payable_fee()}")


def main():
    records = ut.read_file("CourseEnrollments.txt")
    obj = es.EduService()
    obj.read_data(records)

    top = obj.find_top3_courses()
    print("Top 3 Courses:")
    for k, v in top.items():
        print(f"{k} : {v}")

    enrollment_id = input("\nEnter the enrollment id to search: ")
    try:
        ut.validate_enrollment_id(enrollment_id)
        result = obj.search_enrollment(enrollment_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ee.InvalidEnrollmentIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start date to search (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end date to search (DD/MM/YYYY): "))
    cd = obj.find_completion_dates(s, e)

    if not cd:
        print("No enrollments with extended duration found in the specified date range")
        return

    print("Enrollments with more than 35 days duration and their completion dates:")
    for k, v in cd.items():
        print(f"{k} : {v}")

    grade_level = input("\nEnter the grade level for scholarship update: ")
    updated = obj.update_payable_fee(grade_level)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated enrollment details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
