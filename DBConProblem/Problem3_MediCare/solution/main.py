# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import utility as ut
import med_service as ms
import med_exception as me


def display(obj):
    print(f"\nStock Id: {obj.get_stock_id()}")
    print(f"Med Code: {obj.get_med_code()}")
    print(f"Medicine Name: {obj.get_med_name()}")
    print(f"Category: {obj.get_category()}")
    print(f"Unit Price: {obj.get_unit_price()}")
    print(f"Quantity: {obj.get_quantity()}")
    print(f"Manufacture Date: {obj.get_manufacture_date()} 00:00:00")
    print(f"Expiry Date: {obj.get_expiry_date()} 00:00:00")
    print(f"Margin Amount: {obj.get_margin_amount()}")
    print(f"Selling Price: {obj.get_selling_price()}")
    print(f"Total Stock Value: {obj.get_total_stock_value()}")


def main():
    records = ut.read_file("MedicineStock.txt")
    obj = ms.MedService()
    obj.read_data(records)

    top = obj.find_top3_medicines()
    print("Top 3 Medicine Codes:")
    for k, v in top.items():
        print(f"{k} : {v}")

    stock_id = input("\nEnter the stock id to search: ")
    try:
        ut.validate_stock_id(stock_id)
        result = obj.search_stock(stock_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except me.InvalidStockIdException as e:
        print(e.get_message())

    ref = ut.convert_date(input("\nEnter the reference date (DD/MM/YYYY): "))
    days = int(input("Enter the number of days threshold: "))
    near = obj.find_near_expiry(ref, days)

    if not near:
        print("No medicines nearing expiry in the specified window")
        return

    print("Medicines nearing expiry with quantity > 100:")
    for k, v in near.items():
        print(f"{k} : {v}")

    category = input("\nEnter the category for price update: ")
    updated = obj.update_unit_price(category)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated medicine details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
