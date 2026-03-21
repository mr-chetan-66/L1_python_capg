# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

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
    # Step 1: Load and insert all valid utility bill records
    # Write your code here

    # Step 2: Accept bill_id from user, validate, search and display.
    # Invalid id -> print exception message
    # Not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept units_threshold (float) from user, call update_energy_charges(),
    # display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
