# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

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
    # Step 1: Load and insert all valid maintenance records
    # Write your code here

    # Step 2: Accept maintenance_id from user, validate, search and display.
    # Invalid id -> print exception message
    # Not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept operating_hours_threshold (int) from user,
    # call update_parts_cost(), display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
