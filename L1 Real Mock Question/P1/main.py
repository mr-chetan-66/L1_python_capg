# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone

import utility as ut
import car_service as cs

def main():
    # Write the appropriate code here as per the specifications
    f_obj = ut.access_file("CarDetails.txt")

    app = cs.CarService()
    app.read_data(f_obj)

    # Write the appropriate code here as per the specifications to call 'find_top3_rentals' method
    top3 = app.find_top3_rentals()
    print("Top 3 rentals:")
    for k,v in top3.items():
        print(f"{k} : {v}")
    
    print("")
    start_date=input("Enter the start rental date to search:")
    end_date=input("Enter the end rental date to search:")
    start = ut.convert_date(start_date)
    end = ut.convert_date(end_date)

    resDict = app.find_closing_date(start,end)
    if len(resDict) == 0:
        print("No cars taken for rental in the specified date range")
    else:
        print("The closing rental date of cars with the specified rental date is/are:")
        for k,v in resDict.items():
            print("f{k} : {v}")
    
    # Write the appropriate code here as per the specifications
    
if __name__ == "__main__":
    main()
