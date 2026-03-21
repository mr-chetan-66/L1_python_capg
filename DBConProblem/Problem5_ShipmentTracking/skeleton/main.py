# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import shipment_service as ss
import utility as ut


def display(o):
    print(f"\nShipment Id: {o.get_shipment_id()}")
    print(f"Sender Id: {o.get_sender_id()}")
    print(f"Date of Delivery: {o.get_date_of_delivery()} 00:00:00")
    print(f"Weight (kg): {o.get_weight_in_kg()}")
    print(f"Freight Charge: {o.get_freight_charge()}")
    print(f"Handling Charge: {o.get_handling_charge()}")
    print(f"Delay Penalty: {o.get_delay_penalty()}")
    print(f"Tax: {o.get_tax()}")
    print(f"Total Shipping Cost: {o.get_total_shipping_cost()}")


def main():
    # Step 1: Load and insert all valid shipment records
    # Write your code here

    # Step 2: Accept shipment_id from user, validate, search and display.
    # Invalid id -> print exception message
    # Not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept weight_threshold from user, call update_freight(),
    # display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
