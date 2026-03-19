# Please do not change the skelecton code given here.
# Fill the code only in the provided places alone
import utility as ut
import car_service as cs

def main():
    # Write the appropriate code here as per the specifications
    f=ut.access_file("CarDetails.txt")
    obj=cs.CarService()
    obj.read_data(f)
    
    top=obj.find_top3_rentals()
    print("Top 3 rentals:")
    for k,v in top.items():
        print(f"{k} : {v}")
        
    s=ut.convert_date(input("Enter the start rental date to search: "))
    e=ut.convert_date(input("Enter the end rental date to search: "))
    cd=obj.find_closing_date(s,e)
    
    if not cd:
        print("No cars taken for rental in the specified date range")
        return 
    
    print("The closing rental date of cars with th specified rental date is/are:")
    for k,v in cd.items():
        print(f"{k} : {v}")
    
    f.close()
    
if __name__ == "__main__":
    main()
