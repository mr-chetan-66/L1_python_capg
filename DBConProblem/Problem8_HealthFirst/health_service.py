# Please do not change the skeleton code given here.
import utility as ut
import insurance_claim as ic
import oracledb
import health_exception as he

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class HealthService:

    def __init__(self):
        self.__deductible_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line: validate policy_id and claim_id, convert dates,
        # create InsuranceClaim, call calculate_approved_amount(),
        # store deductible in self.__deductible_dict, call add_claim_details().
        # Truncate InsuranceClaim table at start. Return None.
        pass

    def add_claim_details(self, obj):
        # Write your code here
        # Insert into 'InsuranceClaim' table.
        # Column order: claim_id, policy_id, patient_name, policy_type, claim_amount,
        #               claim_date, policy_date, coverage_amount, deductible, approved_amount
        # Return None.
        pass

    def find_top3_policies(self):
        # Write your code here
        # Count appearances of each policy_id. Return top 3 distinct counts, ties included.
        pass

    def search_claim(self, claim_id):
        # Write your code here
        # Return fully populated InsuranceClaim object or None.
        pass

    def find_high_value_claims(self, start_date, end_date):
        # Write your code here
        # Find claims where claim_amount > 100000 and claim_date between start and end.
        # Return {claim_id: claim_amount}. Return empty dict if none.
        pass

    def update_approved_amount(self, policy_type):
        # Write your code here
        # UPDATE: approved_amount = approved_amount * 1.05
        #         coverage_amount = approved_amount * 1.05  (same field, same update)
        # After update SELECT all with that policy_type.
        # Return list of InsuranceClaim objects or None.
        pass
