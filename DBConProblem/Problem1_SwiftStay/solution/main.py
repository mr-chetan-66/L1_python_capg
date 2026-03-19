import utility as ut
import hotel_service as hs
import hotel_exception as he


def display(obj):
    print(f"\nBooking Id: {obj.get_booking_id()}")
    print(f"Guest Name: {obj.get_guest_name()}")
    print(f"Room Number: {obj.get_room_number()}")
    print(f"Room Type: {obj.get_room_type()}")
    print(f"Check-in Date: {obj.get_check_in_date()} 00:00:00")
    print(f"No. of Nights: {obj.get_no_of_nights()}")
    print(f"Base Amount: {obj.get_base_amount()}")
    print(f"Tax Amount: {obj.get_tax_amount()}")
    print(f"Total Amount: {obj.get_total_amount()}")


def main():
    records = ut.read_file("BookingDetails.txt")
    obj = hs.HotelService()
    obj.read_data(records)

    top = obj.find_top3_rooms()
    print("Top 3 Rooms:")
    for k, v in top.items():
        print(f"{k} : {v}")

    booking_id = input("\nEnter the booking id to search: ")
    try:
        ut.validate_booking_id(booking_id)
        result = obj.search_booking(booking_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except he.InvalidBookingIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start check-in date to search (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end check-in date to search (DD/MM/YYYY): "))
    cd = obj.find_checkout_dates(s, e)

    if not cd:
        print("No bookings with extended stays found in the specified date range")
        return

    print("Bookings with more than 5 nights and their checkout dates:")
    for k, v in cd.items():
        print(f"{k} : {v}")

    room_type = input("\nEnter the room type for tax rate update: ")
    updated = obj.update_tax_rates(room_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated booking details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
