### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import event_dao as dao_module
import event_util as util
from exceptions import (EventNotFoundException,
                        EventExpiredException,
                        SeatNotAvailableException,
                        InvalidTicketCountException)


def main():
    conn      = db.get_connection()
    event_dao = dao_module.EventDao(conn)

    print("=" * 60)
    print("          EVENT BOOKING MANAGEMENT SYSTEM")
    print("=" * 60)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve and display all upcoming events with seat summary
    # ----------------------------------------------------------------
    print("\n--- UPCOMING EVENTS ---")

    upcoming = event_dao.retrieve_upcoming_events()
    summary  = util.get_seat_availability_summary(upcoming)

    util.display_upcoming_events(summary)

    # ----------------------------------------------------------------
    # STEP 2 — Book tickets for a selected event
    # ----------------------------------------------------------------
    print("\n--- BOOK TICKETS ---")

    event_id      = int(input("Enter Event ID to Book     : "))
    customer_name = input("Enter Your Name            : ")
    num_tickets   = int(input("Enter Number of Tickets    : "))

    booking_obj = event_dao.book_tickets(event_id, customer_name, num_tickets)

    # Re-fetch event to get the updated booked_seats for the confirmation
    event_obj = event_dao.retrieve_event_by_id(event_id)

    print(f"\nBooking Successful!")
    print(f"Booking ID   : {booking_obj.get_booking_id()}")
    print(f"Total Amount : Rs. {booking_obj.get_total_amount()}")

    # ----------------------------------------------------------------
    # STEP 3 — Export booking confirmation to text file
    # ----------------------------------------------------------------
    print("\n--- EXPORT BOOKING CONFIRMATION ---")

    filename = input("Enter Filename to Save Confirmation : ")

    util.export_booking_confirmation(booking_obj, event_obj, filename)
    print(f"Confirmation saved to {filename}")


if __name__ == '__main__':
    try:
        main()
    except EventNotFoundException as e:
        print(e)
    except EventExpiredException as e:
        print(e)
    except SeatNotAvailableException as e:
        print(e)
    except InvalidTicketCountException as e:
        print(e)
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")
