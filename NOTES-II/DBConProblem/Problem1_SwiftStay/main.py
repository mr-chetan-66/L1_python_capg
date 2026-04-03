# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import utility as ut
import hotel_service as hs
import hotel_exception as he
from datetime import datetime
def display(o):
    print("\n")
    print(f"Booking Id: {o.get_booking_id()}")
    print(f"Guest Name: {o.get_guest_name()}")
    print(f"Room Number: {o.get_room_number()}")
    print(f"Room Type: {o.get_room_type()}")
    print(f"Check-in Date: {o.get_check_in_date()}")
    print(f"No. of Nights: {o.get_no_of_nights()}")
    print(f"Base Amount: {o.get_base_amount()}")
    print(f"Tax Amount: {o.get_tax_amount()}")
    print(f"Total Amount: {o.get_total_amount()}")
    
def main():
    records=ut.read_file("BookingDetails.txt")
    obj=hs.HotelService()
    obj.read_data(records)
   
    top=obj.find_top3_rooms()
    print("Top 3 Rooms:")
    for k,v in top.items():
       print(f"{k} : {v}")
    
    bid=input("Enter the booking id to search: ")
    try:
        ut.validate_booking_id(bid)
        o=obj.search_booking(bid)
        display(o)
        
    except he.InvalidBookingIdException as e:
        print(e.get_message())
    
    s=ut.convert_date(input("Enter the start check-in date to search (DD/MM/YYYY): "))
    e=ut.convert_date(input("Enter the end check-in date to search (DD/MM/YYYY): "))
    
    row=obj.find_checkout_dates(s,e)
    if len(row)==0:
        print("No Room Found")
    else:
        for k,v in row.items():
            print(f"{k} : {v}")
            
    up=input("\nEnter the room type for tax rate update: ")
    upo=obj.update_tax_rates(up)
    
    if not upo:
        print("No record Update")
    else:
        for o in upo:
            display(o)
            
    print("\n--------THANK YOU!------------\n")
    


if __name__ == "__main__":
    main()
