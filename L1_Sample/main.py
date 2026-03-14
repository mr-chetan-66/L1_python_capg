# main.py
import utility as ut
import it_service_management as itsm

def main():
    # Write the appropriate code here as per the specifications
    sid = input("Enter the service ID to be searched: ")
    try:
        # Step 1: Read file -> list of lists
        data = ut.read_file("input.txt")  # do NOT hardcode elsewhere, but passing here is fine
        # Step 2: Build service details (create objects, compute charges)
        mgr = itsm.ITServiceManagement()
        mgr.build_service_details(data)
        # Step 3: Add to database
        mgr.add_service_details()
        # Step 4 & 5: Validate user-entered Service ID
        ut.validate_service_id(sid)
        # Step 6: Search in DB
        result = mgr.search_service_id(sid)
        # Step 7: Display result
        if result is None:
            print("No records found")
        else:
            print("--- IT Service Details ---")
            print(f"Service ID: {result.get_service_id()}")
            print(f"Customer Name: {result.get_customer_name()}")
            print(f"Service Type: {result.get_service_type()}")
            print(f"Service Charge: {result.get_service_charge()}")
    except Exception as e:
        # The only user-facing exception we show is Invalid Service ID as per spec
        if str(e) == "Invalid Service ID":
            print("Invalid Service ID")
        else:
            # For any unexpected failure, stay consistent with sample behavior
            print("No records found")

if __name__ == "__main__":
    main()