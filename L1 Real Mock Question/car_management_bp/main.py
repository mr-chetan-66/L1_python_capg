# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone

import utility as ut
import car_service as cs
import db_setup as dbs

def main():
    # Write the appropriate code here as per the specifications
    dbs.start()
    f=ut.access_file("CarDetails.txt")
    obj=cs.CarService()
    obj.read_data(f)
    top=obj.find_top3_rentals()
    print("Top 3 rentals:")
    for k,v in top.items():
        print(f"{k}: {v}")
    
    start=input("Enter the start rental date to search: ")
    end=input("Enter the end rental date to search: ")
    search=obj.find_closing_date(start,end)

    if len(search)==0:
        print("No car found")
    else:
        print("The closing rental date of cars with the specified rental date is/are")
        for k,v in search.items():
            print(f"{k}: {v}")
    
    f.close()
    
    
if __name__ == "__main__":
    main()
