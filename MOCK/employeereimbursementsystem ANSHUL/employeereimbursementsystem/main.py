# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone
from exception import InvalidRequestIdException
import emp_reimbursement_service as rs

def main():
    # Write the appropriate code here as per the specifications
    
    list_res= rs.EmpReimbursementService.get_emp_reimbursement_details("input.txt")
    rs.EmpReimbursementService.add_reimbursement_details(list_res)
   
    request_id=input("Enter the request id:")
    obj=rs.EmpReimbursementService.search_reimbursement_request(request_id)
    print(f"Request Id: {obj.get_request_id()}")
    print(f" Employee Code: {obj.get_employee_code()}")
    print(f"Date of Travel: {obj.get_date_of_travel()}")
    print(f"No.of Days:{obj.get_no_of_days_of_stay()}")
    print(f"Accomodation Cost: {obj.get_accomodation_cost()}")
    print(f"Dinning Cost: {obj.get_dining_cost()}")
    print(f" Local Travel cost:{obj.get_local_travel_cost()}")
    print(f"Allowances: {obj.get_allowances()}")
    print(f"Total Reimbursement Amount: {obj.get_total_reimbursement_cost()}")

    # Write the appropriate code here fordisplaying the reibursement request details as per the specifications
    
    no_days=int(input("\n\nEnter the no. of days for giving expense increment:"))
    rs.EmpReimbursementService.search_reimbursement_request(no_days)

    # Write the appropriate code here for displaying the increment details as per the specifications
    
   


if __name__ == "__main__":
    main()
