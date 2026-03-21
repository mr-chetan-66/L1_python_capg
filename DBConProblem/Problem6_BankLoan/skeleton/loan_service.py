### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import loan_application as la

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class LoanService:

    def __init__(self):
        self.__loan_list = []

    def get_loan_details(self, input_file):
        """
        Call utility.read_file() with input_file.
        Pass the result to build_loan_list().
        Return __loan_list.
        """
        # Write your code here
        pass

    def build_loan_list(self, records):
        """
        For each record string:
          1. Validate loan_id   -> catch InvalidLoanIdException, print the message
          2. Validate loan_type -> catch InvalidLoanTypeException, print the message
          3. Convert date strings using utility.convert_date()
          4. Create a LoanApplication object
          5. Call calculate_loan_costs() and set all calculated attributes on the object
          6. Append the object to __loan_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_loan_costs(self, loan_amount, tenure_in_months, loan_type, credit_score):
        """
        Return [annual_interest_rate, processing_fee, monthly_emi,
                total_interest, total_repayment] as a list of floats.

        Step 1 – Base interest rate by loan_type:
        +------------+---------------------+
        | Loan Type  | Base Rate (% p.a.)  |
        +------------+---------------------+
        | Home       |         7.0         |
        | Vehicle    |         9.0         |
        | Personal   |        13.0         |
        | Education  |         6.0         |
        +------------+---------------------+

        Step 2 – Credit score discount on the base rate:
        +------------------+------------------+
        | Credit Score     | Discount (% p.a.)|
        +------------------+------------------+
        | 750 and above    |       1.5        |
        | 700 – 749        |       0.75       |
        | 650 – 699        |       0.0        |
        | Below 650        |  +1.0 (surcharge)|
        +------------------+------------------+
        annual_interest_rate = base_rate - discount  (add surcharge if below 650)

        Step 3 – Processing fee by loan_type (flat % of loan_amount):
        +------------+-------------------+
        | Loan Type  | Processing Fee %  |
        +------------+-------------------+
        | Home       |       0.5         |
        | Vehicle    |       1.0         |
        | Personal   |       2.0         |
        | Education  |       0.25        |
        +------------+-------------------+
        processing_fee = loan_amount * processing_fee_pct / 100

        Step 4 – Monthly EMI using standard reducing-balance formula:
            r = annual_interest_rate / 12 / 100   (monthly rate as decimal)
            monthly_emi = loan_amount * r * (1+r)^tenure_in_months
                          / ((1+r)^tenure_in_months - 1)
            Round monthly_emi to 2 decimal places.

        Step 5:
            total_repayment = monthly_emi * tenure_in_months
            total_interest  = total_repayment - loan_amount
            Round both to 2 decimal places.
        """
        # Write your code here
        pass

    def add_loan_details(self, loan_list):
        """
        Insert each LoanApplication object in loan_list into the
        'loan_application' table.
        Column order: loan_id, applicant_id, date_of_application, loan_type,
                      date_of_disbursement, loan_amount, tenure_in_months,
                      credit_score, loan_status, annual_interest_rate,
                      processing_fee, monthly_emi, total_interest, total_repayment
        Returns None.
        """
        # Write your code here
        pass

    def search_loan(self, loan_id):
        """
        Query 'loan_application' by loan_id.
        If found, build and return a fully populated LoanApplication object.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_interest_rate(self, credit_score_threshold):
        """
        For all records in 'loan_application' where credit_score < credit_score_threshold:
          - Increase annual_interest_rate by 0.5 (i.e. add 0.5 percentage points)
          - Recalculate monthly_emi using the NEW annual_interest_rate and existing
            loan_amount and tenure_in_months
            Hint: reuse the EMI formula from calculate_loan_costs()
          - Recalculate total_interest and total_repayment from the new monthly_emi
          - Update all four columns in the database
        Commit the update. Fetch and return all updated LoanApplication objects as a list.
        Return None if no records qualify.
        """
        # Write your code here
        pass
