### event_util.py
### Utility / helper functions for Event Booking — summary, display, file export


# ----------------------------------------------------------------
# COLLECTIONS — build nested seat availability summary dictionary
# ----------------------------------------------------------------
def get_seat_availability_summary(event_list):
    # Returns a nested dict keyed by event_id
    # { event_id: { event_name, total_seats, booked_seats,
    #               available_seats, occupancy_pct } }
    summary = {}
    for e in event_list:
        available    = e.get_total_seats() - e.get_booked_seats()
        occupancy    = round((e.get_booked_seats() / e.get_total_seats()) * 100, 2) \
                       if e.get_total_seats() > 0 else 0.0

        summary[e.get_event_id()] = {
            'event_name'      : e.get_event_name(),
            'total_seats'     : e.get_total_seats(),
            'booked_seats'    : e.get_booked_seats(),
            'available_seats' : available,
            'occupancy_pct'   : occupancy
        }
    return summary


# ----------------------------------------------------------------
# DISPLAY — print seat availability summary to console
# ----------------------------------------------------------------
def display_upcoming_events(summary):
    print("Upcoming Events")
    print("=" * 60)
    for event_id, info in summary.items():
        print(f"Event ID       : {event_id}")
        print(f"Event Name     : {info['event_name']}")
        print(f"Total Seats    : {info['total_seats']}")
        print(f"Booked Seats   : {info['booked_seats']}")
        print(f"Available Seats: {info['available_seats']}")
        print(f"Occupancy      : {info['occupancy_pct']}%")
        print("-" * 60)


# ----------------------------------------------------------------
# FILE WRITE — export booking confirmation to text file
# ----------------------------------------------------------------
def export_booking_confirmation(booking_obj, event_obj, filename):
    try:
        with open(filename, 'w') as f:
            f.write("========== BOOKING CONFIRMATION ==========\n")
            f.write(f"Booking ID    : {booking_obj.get_booking_id()}\n")
            f.write(f"Customer Name : {booking_obj.get_customer_name()}\n")
            f.write(f"Event Name    : {event_obj.get_event_name()}\n")
            f.write(f"Venue         : {event_obj.get_venue()}\n")
            f.write(f"Event Date    : {event_obj.get_event_date().strftime('%d-%m-%Y')}\n")
            f.write(f"Event Time    : {event_obj.get_event_time().strftime('%H:%M')}\n")
            f.write(f"Tickets       : {booking_obj.get_num_tickets()}\n")
            f.write(f"Total Amount  : Rs. {booking_obj.get_total_amount()}\n")
            f.write(f"Booked On     : {booking_obj.get_booking_date().strftime('%d-%m-%Y')}\n")
            f.write("==========================================\n")

    except IOError as e:
        raise IOError(f"Failed to write confirmation file: {e}")
