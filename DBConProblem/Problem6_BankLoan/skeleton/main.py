# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import loan_service as ls
import utility as ut


def display(o):
    print(f"\nLoan Id: {o.get_loan_id()}")
    print(f"Applicant Id: {o.get_applicant_id()}")
    print(f"Loan Type: {o.get_loan_type()}")
    print(f"Date of Disbursement: {o.get_date_of_disbursement()} 00:00:00")
    print(f"Loan Amount: {o.get_loan_amount()}")
    print(f"Tenure (months): {o.get_tenure_in_months()}")
    print(f"Annual Interest Rate: {o.get_annual_interest_rate()}")
    print(f"Processing Fee: {o.get_processing_fee()}")
    print(f"Monthly EMI: {o.get_monthly_emi()}")
    print(f"Total Interest: {o.get_total_interest()}")
    print(f"Total Repayment: {o.get_total_repayment()}")


def main():
    # Step 1: Load and insert all valid loan records
    # Write your code here

    # Step 2: Accept loan_id from user, validate, search and display.
    # Invalid id   -> print exception message
    # Not found    -> print "No record found"
    # Write your code here

    # Step 3: Accept credit_score_threshold from user, call update_interest_rate(),
    # display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
