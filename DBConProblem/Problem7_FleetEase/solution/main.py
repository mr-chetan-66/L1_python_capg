# Please do not change the skeleton code given here.
import utility as ut
import fleet_service as fs
import fleet_exception as fe


def display(obj):
    print(f"\nService Id: {obj.get_service_id()}")
    print(f"Vehicle Name: {obj.get_vehicle_name()}")
    print(f"Vehicle Id: {obj.get_vehicle_id()}")
    print(f"Vehicle Type: {obj.get_vehicle_type()}")
    print(f"Odometer (km): {obj.get_odometer_km()}")
    print(f"Service Date: {obj.get_service_date()} 00:00:00")
    print(f"Parts Cost: {obj.get_parts_cost()}")
    print(f"Labour Cost: {obj.get_labour_cost()}")
    print(f"Total Cost: {obj.get_total_cost()}")


def main():
    records = ut.read_file("VehicleServices.txt")
    obj = fs.FleetService()
    obj.read_data(records)

    top = obj.find_top3_vehicles()
    print("Top 3 Vehicles:")
    for k, v in top.items():
        print(f"{k} : {v}")

    service_id = input("\nEnter the service id to search: ")
    try:
        ut.validate_service_id(service_id)
        result = obj.search_service(service_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except fe.InvalidServiceIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start service date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end service date (DD/MM/YYYY): "))
    hm = obj.find_high_mileage(s, e)

    if not hm:
        print("No high mileage vehicles found in the specified date range")
        return

    print("Services with odometer > 60000 km:")
    for k, v in hm.items():
        print(f"{k} : {v}")

    vehicle_type = input("\nEnter the vehicle type for labour cost update: ")
    updated = obj.update_labour_cost(vehicle_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated service details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
