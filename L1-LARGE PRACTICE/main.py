import utility as ut
import it_service_management as itsm

def main():
    # Write the appropriate code here as per the specifications
    
    itsm_obj = itsm.ITServiceManagement()
    file = "input.txt"
    result_list = ut.read_file(file)
    
    itsm_obj.build_service_details(result_list)
    itsm_obj.add_service_details()
    
    service_id = input("Enter service ID to be searched:")
    result = ut.validate_service_id(service_id)
    if result :
        obj = itsm_obj.search_service_id(service_id)
        if obj is not None:
            
            print("-----IT Service Details------")
            print(f"Service ID: {obj.get_service_id()}")
            print(f"Customer Name: {obj.get_customer_name()}")
            print(f"Service Type: {obj.get_service_type()}")
            print(f"Service Charge:{obj.get_service_charge()}")
        else:
            print("No records found")
    


if __name__ == "__main__":
    main()
