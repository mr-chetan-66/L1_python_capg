# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone


import utility as ut
import med_service as mr
import med_exception as ex

def display(o):
    print("\n")
    print(f"Stock Id: {o.get_stock_id()}")
    print(f"Medicine Code: {o.get_med_code()}")
    print(f"Medicine Name: {o.get_med_name()}")
    print(f"Category: {o.get_category()}")
    print(f"Quantity: {o.get_quantity()}")
    print(f"Manufacture Date: {o.get_manufacture_date()}")
    print(f"Expiry Date: {o.get_expiry_date()}")
    print(f"Selling Price: {o.get_selling_price()}")
    print(f"Total Stock Value: {o.get_total_stock_value()}")
    
    
def main():
    record=ut.read_file("MedicineStock.txt")
    obj=mr.MedService()
    obj.read_data(record)
    
    top=obj.find_top3_medicines()
    print("Top 3 Medicine Codes:")
    for k,v in top.items():
        print(f"{k} : {v}")
        
    sid=input("Enter the stock id to search: ")
    try:
        so=obj.search_stock(sid)
        if so is None:
            print("No stock found")
        else:
            display(so)
    except ex.InvalidStockIdException as e:
        print(e.get_message())
        
    rd=ut.convert_date(input("Enter the reference date (DD/MM/YYYY): "))
    th=int(input("Enter the number of days threshold: "))

    to=obj.find_near_expiry(rd,th)
    if len(to)==0:
        print("No such record")
    else:
        print("Medicines nearing expiry with quantity>100:")
        for k,v in to.items():
            print(f"{k} : {v}")
            
    ct=input("Enter the category for price update: ")
    upo=obj.update_unit_price(ct)
    if upo is None:
        print("No update")
    else:
        print("The updated medicine details are:")
        for o in upo:
            display(o)
    
    print("---------- THANKS YOU! ------------")
if __name__ == "__main__":
    main()
