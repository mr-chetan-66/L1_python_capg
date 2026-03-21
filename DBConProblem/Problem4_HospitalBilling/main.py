# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import exception as ex
import patient_billing_service as sr


def display(o):
    print("\n")
    print(f"Bill Id: {o.get_bill_id()}")
    print(f"Patient Id: {o.get_patient_id()}")
    print(f"Date of Discharge: {o.get_date_of_discharge()}")
    print(f"No. of Days: {o.get_no_of_days()}")
    print(f"Bed Charges: {o.get_bed_charges():.1f}")
    print(f"Treatment Charges: {o.get_treatment_charges():.1f}")
    print(f"Nursing Charges: {o.get_nursing_charges():.1f}")
    print(f"Discount: {o.get_discount():.1f}")
    print(f"Total Bill Amount: {o.get_total_bill_amount():.1f}")

def main():
    obj=sr.PatientBillingService()
    record=obj.get_patient_billing_details("input.txt")
    obj.add_billing_details(record)
    
    bid=input("Enter the Bill Id: ")
    try:
        s_obj=obj.search_billing_record(bid)
        if s_obj is None:
            print("Bill Id not found")
        else:
            display(s_obj)
    except ex.InvalidBillIdException as e:
        print(e.get_message())
        
    nd=int(input("Enter the no. of days for charge increment: "))
    
    upo=obj.update_charges(nd)
    
    if upo is None:
        print("No record update")
    else:
        for o in upo:
            display(o)
            
    


if __name__ == "__main__":
    main()
