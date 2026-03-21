# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import patient_billing_service as s
import utility as ut


def display(o):
    print(f"\nBill Id: {o.get_bill_id()}")
    print(f"Patient Id: {o.get_patient_id()}")
    print(f"Date of Discharge: {o.get_date_of_discharge()} 00:00:00")
    print(f"No. of Days: {o.get_no_of_days()}")
    print(f"Bed Charges: {o.get_bed_charges()}")
    print(f"Treatment Charges: {o.get_treatment_charges()}")
    print(f"Nursing Charges: {o.get_nursing_charges()}")
    print(f"Discount: {o.get_discount()}")
    print(f"Total Bill Amount: {o.get_total_bill_amount()}")


def main():
    # Step 1: Load and insert all valid billing records
    # Write your code here

    # Step 2: Accept bill_id from user, validate it, search and display the record
    # If bill_id is invalid -> print exception message
    # If record not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept no_of_days from user, call update_charges(),
    # and display all updated records. If none updated -> print "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
