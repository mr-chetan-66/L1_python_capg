# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import utility as ut
import shipment_service as ss
import freight_exception as fe


def display(obj):
    print(f"\nShipment Id: {obj.get_shipment_id()}")
    print(f"Client Name: {obj.get_client_name()}")
    print(f"Freight Id: {obj.get_freight_id()}")
    print(f"Service Type: {obj.get_service_type()}")
    print(f"Dispatch Date: {obj.get_dispatch_date()} 00:00:00")
    print(f"No. of Days: {obj.get_no_of_days()}")
    print(f"Weight (kg): {obj.get_weight_kg()}")
    print(f"Base Charge: {obj.get_base_charge()}")
    print(f"Surcharge: {obj.get_surcharge()}")
    print(f"Total Charge: {obj.get_total_charge()}")


def main():
    records = ut.read_file("ShipmentRecords.txt")
    obj = ss.ShipmentService()
    obj.read_data(records)

    top = obj.find_top3_freight()
    print("Top 3 Freight IDs:")
    for k, v in top.items():
        print(f"{k} : {v}")

    shipment_id = input("\nEnter the shipment id to search: ")
    try:
        ut.validate_shipment_id(shipment_id)
        result = obj.search_shipment(shipment_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except fe.InvalidShipmentIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start dispatch date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end dispatch date (DD/MM/YYYY): "))
    dd = obj.find_delivery_dates(s, e)

    if not dd:
        print("No shipments with extended transit found in the specified date range")
        return

    print("Shipments with more than 4 transit days and their delivery dates:")
    for k, v in dd.items():
        print(f"{k} : {v}")

    service_type = input("\nEnter the service type for surcharge update: ")
    updated = obj.update_surcharge(service_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated shipment details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
