### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import vehicle_dao as dao
import vehicle_util as util
from datetime import date


def main():
    conn = db.get_connection()

    print("=" * 42)
    print("    VEHICLE INSURANCE MANAGEMENT SYSTEM")
    print("=" * 42)

    vehicle_type = input("Enter Vehicle Type (car/bike/truck/bus): ")

    # Validate vehicle type
    if not util.is_valid_vehicle_type(vehicle_type):
        print("Invalid Vehicle Type")
        return

    # Retrieve all vehicles with expired insurance
    expired_vehicles = dao.retrieve_expired_insurance_vehicles(vehicle_type, conn)

    if not expired_vehicles:
        print("No vehicles with expired insurance found")
        return

    print("\nTotal Expired Insurance Vehicles :", util.get_result_count(expired_vehicles))
    print("-" * 42)

    # Display each vehicle with days overdue
    for vehicle in expired_vehicles:
        util.display_vehicle(vehicle)
        print("Days Overdue       :", util.get_days_overdue(vehicle))
        print("-" * 42)

    # Highlight most overdue vehicle
    most_overdue = util.get_most_overdue(expired_vehicles)
    print("=" * 42)
    print("Most Overdue Vehicle:")
    print("  Vehicle ID :", most_overdue.get_vehicle_id())
    print("  Owner      :", most_overdue.get_owner_name())
    print("  Days Overdue:", util.get_days_overdue(most_overdue))
    print("=" * 42)

    # Step 2 — Renew insurance for a selected vehicle
    vehicle_id      = input("\nEnter Vehicle ID to Renew Insurance : ")
    new_expiry_str  = input("Enter New Expiry Date (YYYY-MM-DD)  : ")

    # Parse the new expiry date
    try:
        new_expiry_date = date.fromisoformat(new_expiry_str)
    except ValueError:
        print("Invalid Date Format")
        return

    # Validate the renewal date is in the future
    if not util.is_valid_renewal_date(new_expiry_date):
        print("Renewal Date Must Be In The Future")
        return

    result = dao.renew_insurance(vehicle_id, new_expiry_date, conn)
    print("\nStatus :", result)

    # Show updated vehicle details after renewal
    if result == "Insurance Renewed Successfully":
        updated_vehicle = dao.retrieve_vehicle_by_id(vehicle_id, conn)
        print("\nUpdated Vehicle Details:")
        util.display_vehicle(updated_vehicle)


if __name__ == '__main__':
    main()
