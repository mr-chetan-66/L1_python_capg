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
    svc = ss.ShipmentService()
    records = svc.get_shipment_details("input.txt")
    svc.add_shipment_details(records)

    shipment_id = input("Enter the Shipment Id: ")
    try:
        ut.validate_shipment_id(shipment_id)
        result = svc.search_shipment(shipment_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidShipmentIdException as e:
        print(e.get_message())

    weight_threshold = float(input("\n\nEnter the weight threshold (kg) for freight increment: "))
    updated = svc.update_freight(weight_threshold)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
