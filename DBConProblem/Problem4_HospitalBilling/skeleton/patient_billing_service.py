### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import patient_billing as pb

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

# Creating Connection
conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class PatientBillingService:

    def __init__(self):
        self.__patient_billing_list = []

    def get_patient_billing_details(self, input_file):
        """
        Read the input file via utility.read_file(), pass the result to
        build_patient_billing_list(), and return the __patient_billing_list.
        """
        # Write your code here
        pass

    def build_patient_billing_list(self, records):
        """
        For each record string in the list:
          1. Validate bill_id  -> catch InvalidBillIdException and print the message
          2. Validate ward_type -> catch InvalidWardTypeException and print the message
          3. Convert date strings using utility.convert_date()
          4. Create a PatientBilling object
          5. Call calculate_billing_costs() and set all cost attributes on the object
          6. Append the object to __patient_billing_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_billing_costs(self, no_of_days, ward_type):
        """
        Calculate and return [bed_charges, treatment_charges, nursing_charges,
                               discount, total_bill_amount] as a list of floats.

        Cost table (per day):
        +--------------+----------+-----------+----------+----------+
        | Ward Type    | Bed/Day  | Trtmt/Day | Nurs/Day | Disc %   |
        +--------------+----------+-----------+----------+----------+
        | General      |    500   |    800    |   300    |   5%     |
        | Semi-Private |   1500   |   1500    |   600    |   3%     |
        | Private      |   3000   |   2500    |  1000    |   2%     |
        | ICU          |   8000   |   5000    |  2000    |   0%     |
        +--------------+----------+-----------+----------+----------+

        gross = (bed + treatment + nursing) charges
        discount = gross * discount_percent / 100
        total_bill_amount = gross - discount
        """
        # Write your code here
        pass

    def add_billing_details(self, billing_list):
        """
        Insert each PatientBilling object in billing_list into the
        'patient_billing' table in the database.
        Column order: bill_id, patient_id, date_of_admission, ward_type,
                      date_of_discharge, no_of_days, treatment_code, insurance_status,
                      bed_charges, treatment_charges, nursing_charges, discount,
                      total_bill_amount
        Returns None.
        """
        # Write your code here
        pass

    def search_billing_record(self, bill_id):
        """
        Search the 'patient_billing' table for the given bill_id.
        If found, construct and return a PatientBilling object with all attributes set.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_charges(self, no_days):
        """
        For all records in 'patient_billing' where no_of_days > no_days:
          - Increase bed_charges by 15%
          - Increase nursing_charges by 15%
          - Recalculate total_bill_amount = new_bed + treatment_charges + new_nursing - discount
        Commit the update, then fetch and return all updated records as a list of
        PatientBilling objects. Return None if no records are updated.
        """
        # Write your code here
        pass
