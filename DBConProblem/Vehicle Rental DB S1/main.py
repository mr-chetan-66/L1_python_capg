### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import rental_dao as dao_module
import rental_util as util
from datetime import date


def main():
    conn       = db.get_connection()
    rental_dao = dao_module.RentalDao(conn)

    print("=" * 42)
    print("       VEHICLE RENTAL MANAGEMENT SYSTEM")
    print("=" * 42)

    # ----------------------------------------------------------------
    # STEP 1 — Create a new rental
    # ----------------------------------------------------------------
    print("\n--- CREATE NEW RENTAL ---")

    rental_id   = int(input("Enter Rental ID      : "))
    customer_id = int(input("Enter Customer ID    : "))
    vehicle_id  = int(input("Enter Vehicle ID     : "))

    start_str   = input("Enter Start Date (YYYY-MM-DD) : ")
    end_str     = input("Enter End Date   (YYYY-MM-DD) : ")

    try:
        start_date = date.fromisoformat(start_str)
        end_date   = date.fromisoformat(end_str)
    except ValueError:
        print("Invalid Date Format")
        return

    daily_rate  = float(input("Enter Daily Rate     : "))

    # Validations
    if not util.is_valid_date_range(start_date, end_date):
        print("End Date Must Be After Start Date")
        return

    if not util.is_valid_daily_rate(daily_rate):
        print("Invalid Daily Rate")
        return

    # Create the rental
    new_rental = rental_dao.create_rental(
        rental_id, customer_id, vehicle_id,
        start_date, end_date, daily_rate
    )

    if new_rental is None:
        print("Rental Creation Failed")
        return

    print("\nRental Created Successfully!")
    util.display_rental(new_rental)

    # ----------------------------------------------------------------
    # STEP 2 — View all pending rentals for the customer
    # ----------------------------------------------------------------
    print("\n--- PENDING RENTALS FOR CUSTOMER", customer_id, "---")

    pending = rental_dao.retrieve_pending_rentals(customer_id)

    if not pending:
        print("No Pending Rentals Found")
    else:
        print("Total Pending Rentals  :", util.get_result_count(pending))
        print("Total Pending Amount   :", util.get_total_pending_amount(pending))

        longest = util.get_longest_rental(pending)
        print("Longest Rental Days    :", util.calculate_rental_days(longest))
        print("-" * 42)

        for rental in pending:
            util.display_rental(rental)
            print("Status Label           :", util.get_payment_status_label(rental))
            print("-" * 42)

    # ----------------------------------------------------------------
    # STEP 3 — Mark a rental as Paid
    # ----------------------------------------------------------------
    print("\n--- MARK RENTAL AS PAID ---")
    pay_id = int(input("Enter Rental ID to Mark as Paid (0 to skip) : "))

    if pay_id != 0:
        if not util.is_valid_rental_id(pay_id):
            print("Invalid Rental ID")
            return

        pay_result = rental_dao.mark_as_paid(pay_id)
        print("Payment Status :", pay_result)

        if pay_result == "Payment Updated Successfully":
            updated = rental_dao.retrieve_rental_by_id(pay_id)
            print("Updated Rental:")
            util.display_rental(updated)

    # ----------------------------------------------------------------
    # STEP 4 — Cancel a pending rental
    # ----------------------------------------------------------------
    print("\n--- CANCEL A RENTAL ---")
    cancel_id = int(input("Enter Rental ID to Cancel (0 to skip) : "))

    if cancel_id != 0:
        if not util.is_valid_rental_id(cancel_id):
            print("Invalid Rental ID")
            return

        cancel_result = rental_dao.cancel_rental(cancel_id)
        print("Cancellation Status :", cancel_result)

        # Show updated pending list after cancellation
        if cancel_result == "Rental Cancelled Successfully":
            updated_pending = rental_dao.retrieve_pending_rentals(customer_id)
            print("\nUpdated Pending Rentals Count :", util.get_result_count(updated_pending))
            print("Updated Pending Amount        :", util.get_total_pending_amount(updated_pending))


if __name__ == '__main__':
    main()
