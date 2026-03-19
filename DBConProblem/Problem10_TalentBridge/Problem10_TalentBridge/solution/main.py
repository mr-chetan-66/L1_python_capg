# Please do not change the skeleton code given here.
import utility as ut
import talent_service as ts
import talent_exception as te


def display(obj):
    print(f"\nApplication Id: {obj.get_application_id()}")
    print(f"Applicant Name: {obj.get_applicant_name()}")
    print(f"Job Code: {obj.get_job_code()}")
    print(f"Job Title: {obj.get_job_title()}")
    print(f"Experience Grade: {obj.get_experience_grade()}")
    print(f"Years of Experience: {obj.get_years_exp()}")
    print(f"Application Date: {obj.get_application_date()} 00:00:00")
    print(f"Base Salary: {obj.get_base_salary()}")
    print(f"Experience Bonus: {obj.get_experience_bonus()}")
    print(f"Offered Salary: {obj.get_offered_salary()}")


def main():
    records = ut.read_file("JobApplications.txt")
    obj = ts.TalentService()
    obj.read_data(records)

    top = obj.find_top3_jobs()
    print("Top 3 Job Codes:")
    for k, v in top.items():
        print(f"{k} : {v}")

    application_id = input("\nEnter the application id to search: ")
    try:
        ut.validate_application_id(application_id)
        result = obj.search_application(application_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except te.InvalidApplicationIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start application date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end application date (DD/MM/YYYY): "))
    sr = obj.find_senior_applicants(s, e)

    if not sr:
        print("No senior applicants found in the specified date range")
        return

    print("Applicants with more than 7 years of experience:")
    for k, v in sr.items():
        print(f"{k} : {v}")

    grade = input("\nEnter the experience grade for salary update: ")
    updated = obj.update_offered_salary(grade)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated application details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
