import utility as ut
import it_service_management as itsm

def main():
    # Write the appropriate code here as per the specifications
    data = ut.read_file("input.txt")
    obj = itsm.ITServiceManagement()
    obj.build_service_details(data)
    obj.add_service_details()

    service_id = input("Enter the service ID to be searched: ")
    # # Write the appropriate code here as per the specifications
    valid = ut.validate_service_id(service_id)
    if valid == True:
        data = obj.search_service_id(service_id)
        if data is None:
            print("No records found")
        else:
            print()
            print("---IT Service Details---")
            print(f"Service ID: {data.get_service_id()}")
            print(f"Customer Name: {data.get_customer_name()}")
            print(f"Service Type: {data.get_service_type()}")
            print(f"Service Charge: {data.get_service_charge()}")
    else:
        print("Invalid Service ID")
    
    
   
    
    
    
    
if __name__ == "__main__":
    main()
