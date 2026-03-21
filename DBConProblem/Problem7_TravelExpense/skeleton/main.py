# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import travel_expense_service as ts
import utility as ut


def display(o):
    print(f"\nExpense Id: {o.get_expense_id()}")
    print(f"Employee Id: {o.get_employee_id()}")
    print(f"City Tier: {o.get_city_tier()}")
    print(f"Date of Return: {o.get_date_of_return()} 00:00:00")
    print(f"No. of Days: {o.get_no_of_days()}")
    print(f"Travel Mode: {o.get_travel_mode()}")
    print(f"Flight/Transport Cost: {o.get_flight_or_transport_cost()}")
    print(f"Hotel Cost: {o.get_hotel_cost()}")
    print(f"Meal Cost: {o.get_meal_cost()}")
    print(f"Incidental Allowance: {o.get_incidental_allowance()}")
    print(f"Total Expense: {o.get_total_expense()}")


def main():
    # Step 1: Load and insert all valid travel expense records
    # Write your code here

    # Step 2: Accept expense_id from user, validate, search and display.
    # Invalid id -> print exception message
    # Not found  -> print "No record found"
    # Write your code here

    # Step 3: Accept no_of_days_threshold from user, call update_meal_cost(),
    # display updated records or "No Records updated"
    # Write your code here
    pass


if __name__ == "__main__":
    main()
