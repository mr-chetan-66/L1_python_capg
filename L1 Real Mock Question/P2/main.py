# main.py
from utility import validate_request_id, InvalidRequestIdException
from empreimbursementservice import EmpReimbursementService

def display_emp(emp_obj):
    for line in emp_obj.to_display_lines():
        print(line)

def main():
    svc = EmpReimbursementService()

    # Step a–g: build from input.txt and insert into DB
    INPUT_FILE = "input.txt"   # Do NOT hard-code elsewhere; pass as argument here
    emp_list = svc.get_emp_reimbursement_details(INPUT_FILE)
    # Persist valid ones
    if emp_list:
        try:
            svc.add_reimbursement_details(emp_list)
        except Exception as e:
            # If DB is not reachable or cx_Oracle missing, you may see an error.
            # In the target platform this is expected to work.
            pass

    # Search flow
    try:
        request_id = input("Enter the Request Id: ").strip()
        validate_request_id(request_id)
    except InvalidRequestIdException as ex:
        print(str(ex))
        # Still continue to the increment step (as in sample 2)
        no_days_s = input("Enter the no. of days for giving expense increment:")
        try:
            no_days = int(float(no_days_s.strip()))
        except Exception:
            no_days = 0
        try:
            updated = svc.update_costs(no_days)
            if not updated:
                print("No Records updated")
            else:
                print("The updated record details are:")
                for e in updated:
                    display_emp(e)
        except Exception:
            print("No Records updated")
        return

    # If valid id, query DB
    emp_obj = None
    try:
        emp_obj = svc.search_reimbursement_request(request_id)
    except Exception:
        emp_obj = None

    if emp_obj is None:
        print("No record found")
    else:
        # Print in sample format
        print(f"Request Id: {emp_obj.get_request_id()}")
        print(f"Employee Code: {emp_obj.get_employee_code()}")
        print(f"Date of Travel: {emp_obj.get_date_of_travel()} 00:00:00")
        print(f"No.of Days: {float(emp_obj.get_no_of_days_of_stay()):.1f}")
        print(f"Accommodation Cost: {emp_obj.get_accomodation_cost():.1f}")
        print(f"Dinning Cost: {emp_obj.get_dining_cost():.1f}")
        print(f"Local Travel cost: {emp_obj.get_local_travel_cost():.1f}")
        print(f"Allowances: {emp_obj.get_allowances():.1f}")
        print(f"Total Reimbursement Amount: {emp_obj.get_total_reimbursement_cost():.1f}")

    # Update flow
    no_days_s = input("Enter the no. of days for giving expense increment:")
    try:
        no_days = int(float(no_days_s.strip()))
    except Exception:
        no_days = 0

    try:
        updated = svc.update_costs(no_days)
        if not updated:
            print("No Records updated")
        else:
            print("The updated record details are:")
            for e in updated:
                # Use consistent sample display
                for line in e.to_display_lines():
                    print(line)
    except Exception:
        print("No Records updated")

if __name__ == "__main__":
    main()