# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import freight_exception as ex
import utility as ut
import shipment_service as sr

def display(o):
    print("\n")
    print(f"Shipment Id: {o.get_shipment_id()}")
    print(f"Freight Id: {o.get_freight_id()}")
    print(f"Client Name: {o.get_client_name()}")
    print(f"Wight(kg): {o.get_weight_kg()}")
    print(f"Service Type: {o.get_service_type()}")
    print(f"Base Charge: {o.get_base_charge()}")
    print(f"Surcharge: {o.get_surcharge()}")
    print(f"Total Charge: {o.get_total_charge()}")

def main():
    record=ut.read_file("ShipmentRecords.txt")
    obj=sr.ShipmentService()
    list_obj=obj.read_data(record)
    obj.add_shipment_details(list_obj)
    top=obj.find_top3_freight()
    print("Top 3 Freight IDs:")
    for k,v in top.items():
        print(f"{k} : {v}")
    
    sid=input("Enter the shipment id to search: ")
    try:
        ut.validate_shipment_id(sid)
        sobj=obj.search_shipment(sid)
        if sobj is None:
            print("Shipment Id not found")
        else:
            display(sobj)
    except ex.InvalidShipmentIdException as e:
        print(e.get_message())
        
    s=ut.convert_date(input("Enter the start dispatch date (DD/MM/YYYY): "))
    e=ut.convert_date(input("Enter the end dispatch date (DD/MM/YYYY): "))
    
    doj=obj.find_delivery_dates(s,e)
    if len(doj)==0:
        print("No Shipment found")
    else:
        print("Shipments with more than 4 transit days and their delievery dates:")
        for k,v in doj .items():
            print(f"{k} : {v.strftime("%Y-%m-%d")}")
            
    
    up=input("Enter the service type for surcharge update: ")
    upo=obj.update_surcharge(up)
    
    if upo is None:
        print("No shipment update")
    else:
        print("The updated shipment details are:")
        for o in upo:
            display(o)            
    
    print("----------- Thanks You! ------------")
        

if __name__ == "__main__":
    main()
