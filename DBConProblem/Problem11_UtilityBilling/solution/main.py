import exception as ex
import utility_bill_service as us
import utility as ut


def display(o):
    print(f"\nBill Id: {o.get_bill_id()}")
    print(f"Consumer Id: {o.get_consumer_id()}")
    print(f"Consumer Type: {o.get_consumer_type()}")
    print(f"Reading Date: {o.get_reading_date()} 00:00:00")
    print(f"Units Consumed: {o.get_units_consumed()}")
    print(f"Connection Type: {o.get_connection_type()}")
    print(f"Energy Charge: {o.get_energy_charge()}")
    print(f"Fixed Charge: {o.get_fixed_charge()}")
    print(f"Tax: {o.get_tax()}")
    print(f"Total Bill Amount: {o.get_total_bill_amount()}")


def main():
    svc = us.UtilityBillService()
    records = svc.get_utility_bill_details("input.txt")
    svc.add_utility_bill_details(records)

    bill_id = input("Enter the Bill Id: ")
    try:
        ut.validate_bill_id(bill_id)
        result = svc.search_bill(bill_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidBillIdException as e:
        print(e.get_message())

    units_threshold = float(input("\n\nEnter the units threshold for energy charge update: "))
    updated = svc.update_energy_charges(units_threshold)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
