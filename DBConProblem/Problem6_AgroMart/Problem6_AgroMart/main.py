# Please do not change the skeleton code given here.
import utility as ut
import agro_service as ag
import agro_exception as ae


def display(obj):
    print(f"\nAgri Id: {obj.get_agri_id()}")
    print(f"Crop Code: {obj.get_crop_code()}")
    print(f"Crop Name: {obj.get_crop_name()}")
    print(f"Crop Type: {obj.get_crop_type()}")
    print(f"Season: {obj.get_season()}")
    print(f"Harvest Date: {obj.get_harvest_date()} 00:00:00")
    print(f"Quantity (kg): {obj.get_quantity_kg()}")
    print(f"Base Price: {obj.get_base_price()}")
    print(f"Seasonal Premium: {obj.get_seasonal_premium()}")
    print(f"Selling Price: {obj.get_selling_price()}")
    print(f"Total Value: {obj.get_total_value()}")


def main():
    records = ut.read_file("CropInventory.txt")
    obj = ag.AgroService()
    obj.read_data(records)

    top = obj.find_top3_crops()
    print("Top 3 Crop Codes:")
    for k, v in top.items():
        print(f"{k} : {v}")

    agri_id = input("\nEnter the agri id to search: ")
    try:
        ut.validate_agri_id(agri_id)
        result = obj.search_crop(agri_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except ae.InvalidAgriIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start harvest date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end harvest date (DD/MM/YYYY): "))
    bulk = obj.find_bulk_stock(s, e)

    if not bulk:
        print("No bulk stock found in the specified harvest date range")
        return

    print("Crops with quantity > 4000 kg:")
    for k, v in bulk.items():
        print(f"{k} : {v}")

    season = input("\nEnter the season for base price update: ")
    updated = obj.update_base_price(season)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated crop details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
