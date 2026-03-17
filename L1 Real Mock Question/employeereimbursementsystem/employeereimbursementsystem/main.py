# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone
import exception as ex
import emp_reimbursement_service as r
import utility as ut

def display(o):
    print(f"\nRequest Id: {o.get_request_id()}")
    print(f"Employee Code: {o.get_employee_code()}")
    print(f"Date of Travel: {o.get_date_of_travel()} 00:00:00")
    print(f"No.of Days{o.get_no_of_days_of_stay()}")
    print(f"Accomodation Cost: {o.get_accomodation_cost()}")
    print(f"Dinning Cost: {o.get_dining_cost()}")
    print(f"Local Travel cost: {o.get_local_travel_cost()}")
    print(f"Allowances: {o.get_allowances()}")
    print(f"Total Reimbursement Amount: {o.get_total_reimbursement_cost()}")

def main():
    # Write the appropriate code here as per the specifications
    obj=r.EmpReimbursementService()
    request=obj.get_emp_reimbursement_details("input.txt")
    obj.add_reimbursement_details(request)
    
    request_id=input("Enter the request id:")
    try:
        ut.validate_request_id(request_id)
        sobj=obj.search_reimbursement_request(request_id)
        if sobj is None:
            print("No record found")
        else:
            display(sobj)
    except ex.InvalidRequestIdException as e:
        print(e.get_message)
    

    # Write the appropriate code here fordisplaying the reibursement request details as per the specifications
    
    no_days=int(input("\n\nEnter the no. of days for giving expense increment:"))
    uobj=obj.update_costs(no_days)
    if uobj is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in uobj:
            display(o)
            
    # Write the appropriate code here for displaying the increment details as per the specifications
    
if __name__ == "__main__":
    main()
