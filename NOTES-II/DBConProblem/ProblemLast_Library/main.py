### DO NOT ALTER THE GIVEN TEMPLATE. FILL CODE ONLY IN THE PROVIDED PLACES.

import book_lending_service as bs
import utility as ut
from exception import InvalidLendingIdException


def display(obj):
    print("\n")
    print(f"Lending Id        : {obj.get_lending_id()}")
    print(f"Student Id        : {obj.get_student_id()}")
    print(f"Membership Type   : {obj.get_membership_type()}")
    print(f"Due Date          : {obj.get_due_date()}")
    print(f"No. of Books      : {obj.get_no_of_books()}")
    print(f"Late Days         : {obj.get_late_days()}")
    print(f"Base Charge       : {obj.get_base_charge():.2f}")
    print(f"Late Fine         : {obj.get_late_fine():.2f}")
    print(f"Discount          : {obj.get_discount():.2f}")
    print(f"Net Amount        : {obj.get_net_amount():.2f}")


def main():

    # Step 1: Create a BookLendingService object
    # Write your code here

    # Step 2: Load lending records from "input.txt" and store them in DB
    # Write your code here

    # Step 3: Accept a lending_id from the user.
    #         Validate it using ut.validate_lending_id().
    #         If valid, search for the record and display it using display().
    #         If not found, print "No record found".
    #         If InvalidLendingIdException is raised, print the exception message.
    lending_id = input("Enter the Lending Id: ")
    try:
        # Write your code here
        pass
    except InvalidLendingIdException as e:
        # Write your code here
        pass

    # Step 4: Accept min_books from the user (integer).
    #         Call update_fines() and display all updated records.
    #         If no records were updated, print "No Records Updated".
    min_books = int(input("\nEnter the minimum number of books for fine increment: "))
    # Write your code here


if __name__ == "__main__":
    main()
