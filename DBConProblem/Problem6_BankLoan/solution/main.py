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
    svc = ls.LoanService()
    records = svc.get_loan_details("input.txt")
    svc.add_loan_details(records)

    loan_id = input("Enter the Loan Id: ")
    try:
        ut.validate_loan_id(loan_id)
        result = svc.search_loan(loan_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidLoanIdException as e:
        print(e.get_message())

    credit_threshold = int(input("\n\nEnter the credit score threshold for interest rate update: "))
    updated = svc.update_interest_rate(credit_threshold)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
