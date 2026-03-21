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
    svc = ts.TravelExpenseService()
    records = svc.get_travel_expense_details("input.txt")
    svc.add_travel_expense_details(records)

    expense_id = input("Enter the Expense Id: ")
    try:
        ut.validate_expense_id(expense_id)
        result = svc.search_expense(expense_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ex.InvalidExpenseIdException as e:
        print(e.get_message())

    no_days = int(input("\n\nEnter the no. of days threshold for meal cost update: "))
    updated = svc.update_meal_cost(no_days)
    if updated is None:
        print("No Records updated")
    else:
        print("\nThe updated record details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
