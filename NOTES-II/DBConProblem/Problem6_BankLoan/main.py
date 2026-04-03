# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import loan_service as ls
import utility as ut


def display(o):
    print(f"\nLoan Id: {o.get_loan_id()}")
    print(f"Applicant Id: {o.get_applicant_id()}")
    print(f"Loan Type: {o.get_loan_type()}")
    print(f"Date of Disbursement: {o.get_date_of_disbursement()}")
    print(f"Loan Amount: {o.get_loan_amount()}")
    print(f"Tenure (months): {o.get_tenure_in_months()}")
    print(f"Annual Interest Rate: {o.get_annual_interest_rate()}")
    print(f"Processing Fee: {o.get_processing_fee()}")
    print(f"Monthly EMI: {o.get_monthly_emi()}")
    print(f"Total Interest: {o.get_total_interest()}")
    print(f"Total Repayment: {o.get_total_repayment()}")


def main():
    obj=ls.LoanService()
    record=obj.get_loan_details("input.txt")
    obj.add_loan_details(record)
    
    lid=input("Enter the Loan Id: ")
    try:
        ut.validate_loan_id(lid)
        lo=obj.search_loan(lid)
        if lo is None:
            print("Loan Id not found")
        else:
            display(lo)
    except ex.InvalidLoanIdException as e:
        print(e.get_message())
        
    cc=int(input("Enter the credit score threshold for interest rate update: "))
    rows=obj.update_interest_rate(cc)
    if rows is None:
        print("No record Update")
    else:
        for obj in rows:
            display(obj)
    
if __name__ == "__main__":
    main()
