# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone

import emp_reimbursement_service as rs
import utility as ut
from exception import InvalidRequestIdException

def display(o):
    print(f"Request Id: {o.get_request_id()}")
    print(f"Employee Code: {o.get_employee_code()}")
    print(f"Date of Travel: {o.get_date_of_travel()} 00:00:00")
    print(f"No.of Days: {o.get_no_of_days_of_stay()}")
    print(f"Accommodation Cost: {o.get_accomodation_cost()}")
    print(f"Dinning Cost: {o.get_dining_cost()}")
    print(f"Local Travel cost: {o.get_allowances()}")
    print(f"Allowances: {o.get_local_travel_cost()}")
    print(f"Total Reimbursement Amount: {o.get_total_reimbursement_cost()}")

def main():
    # Write the appropriate code here as per the specifications
    obj=rs.EmpReimbursementService()
    record_l=obj.get_emp_reimbursement_details("input.txt")
    obj.add_reimbursement_details(record_l)
    
    rid=input("Enter the request id:")
    try:
        if ut.validate_request_id(rid):
            srid=obj.search_reimbursement_request(rid)
            if srid is not None:
                display(srid)
            else:
                print("No record found")
    except InvalidRequestIdException as e:
        print(e.get_message())
        
    
    # Write the appropriate code here fordisplaying the reibursement request details as per the specifications
    no_days=int(input("\n\nEnter the no. of days for giving expense increment:"))
    
    # Write the appropriate code here for displaying the increment details as per the specifications
    l_obj=obj.update_costs(no_days)
    
    if l_obj is None:
        print("No record update")
    else:
        print("\nThe updated record details are:")
        for o in l_obj:
            display(o)
   
    f.close()

if __name__ == "__main__":
    main()
