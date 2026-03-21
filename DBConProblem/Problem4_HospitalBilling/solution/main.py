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
    svc = s.PatientBillingService()
    records = svc.get_patient_billing_details("input.txt")
    svc.add_billing_details(records)

    bill_id = input("Enter the Bill Id: ")
    try:
        ut.validate_bill_id(bill_id)
        result = svc.search_billing_record(bill_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidBillIdException as e:
        print(e.get_message())

    no_days = int(input("\n\nEnter the no. of days for charge increment: "))
    updated = svc.update_charges(no_days)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
