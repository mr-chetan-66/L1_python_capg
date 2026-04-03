# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone

import exception as ex
import shipment_service as sr
import utility as ut

def display(o):
    print("\n")
    print(f"Shipment Id: : {o.get_shipment_id()}")
    print(f"Sender Id: {o.get_sender_id()}")
    print(f"Date of Delivery: {o.get_date_of_delivery()}")
    print(f"Weight (Kg): {o.get_weight_in_kg()}")
    print(f"Freight Charge: {o.get_freight_charge():.1f}")
    print(f"Handling Charge: {o.get_handling_charge():.1f}")
    print(f"Delay Penalty: {o.get_delay_penalty():.1f}")
    print(f"Tax: {o.get_tax():.1f}")
    print(f"Total Shipping Cost: {o.get_total_shipping_cost():.1f}")


def main():
    obj=sr.ShipmentService()
    record=obj.get_shipment_details("input.txt")
    obj.add_shipment_details(record)
    
    sid=input("Enter the Shipment Id: ")
    try:
        ut.validate_shipment_id(sid)
        row=obj.search_shipment(sid)
        if row is None:
            print("No Shipment Found")
        else:
            display(row)
    except ex.InvalidShipmentIdException as e:
        print(e.get_message())

    up=float(input("Enter the weight threshold (kg) for freight increment: "))
    
    upo=obj.update_freight(up)
    
    if upo is None:
        print("No update done")
    else:
        for o in upo:
            display(o)
    
if __name__ == "__main__":
    main()
