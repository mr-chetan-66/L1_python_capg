import train_management as tm
 
def main():
    tms = tm.TrainManagementSystem()
   
    source = input("Enter the source\n")
    destination = input("Enter the destination\n")
    coach_type = input("Enter the coach type\n")
   
    valid_coaches = ['ac1', 'ac2', 'ac3', 'sleeper', 'seater']
   
    # Case-insensitive validation
    if coach_type.lower() not in valid_coaches:
        print("Invalid Coach Type")
        return
   
    trains = tms.retrieve_train_details(coach_type.lower(), source, destination)
   
    if not trains:
        print("No trains found")
    else:
        for train in trains:
            print(f"{train.get_train_number()}  {train.get_train_name()}")
 
 
if __name__ == '__main__':
    main()