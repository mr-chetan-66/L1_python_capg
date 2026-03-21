import exception as ex
import maintenance_service as ms
import utility as ut


def display(o):
    print(f"\nMaintenance Id: {o.get_maintenance_id()}")
    print(f"Equipment Id: {o.get_equipment_id()}")
    print(f"Equipment Type: {o.get_equipment_type()}")
    print(f"Date of Next Service: {o.get_date_of_next_service()} 00:00:00")
    print(f"Operating Hours: {o.get_operating_hours()}")
    print(f"Technician Grade: {o.get_technician_grade()}")
    print(f"Base Service Cost: {o.get_base_service_cost()}")
    print(f"Parts Cost: {o.get_parts_cost()}")
    print(f"Technician Fee: {o.get_technician_fee()}")
    print(f"Overhaul Surcharge: {o.get_overhaul_surcharge()}")
    print(f"Total Maintenance Cost: {o.get_total_maintenance_cost()}")


def main():
    svc = ms.MaintenanceService()
    records = svc.get_maintenance_details("input.txt")
    svc.add_maintenance_details(records)

    maintenance_id = input("Enter the Maintenance Id: ")
    try:
        ut.validate_maintenance_id(maintenance_id)
        result = svc.search_maintenance_record(maintenance_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidMaintenanceIdException as e:
        print(e.get_message())

    hours_threshold = int(input("\n\nEnter the operating hours threshold for parts cost update: "))
    updated = svc.update_parts_cost(hours_threshold)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
