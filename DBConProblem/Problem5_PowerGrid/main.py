# Please do not change the skeleton code given here.
# Fill the code only in the provided places alone
import utility as ut
import power_service as ps
import power_exception as pe


def display(obj):
    print(f"\nReading Id: {obj.get_reading_id()}")
    print(f"Consumer Name: {obj.get_consumer_name()}")
    print(f"Meter Code: {obj.get_meter_code()}")
    print(f"Consumer Type: {obj.get_consumer_type()}")
    print(f"Units Consumed: {obj.get_units_consumed()}")
    print(f"Reading Date: {obj.get_reading_date()} 00:00:00")
    print(f"Billing Date: {obj.get_billing_date()} 00:00:00")
    print(f"Energy Charge: {obj.get_energy_charge()}")
    print(f"Fixed Charge: {obj.get_fixed_charge()}")
    print(f"Total Bill: {obj.get_total_bill()}")


def main():
    records = ut.read_file("MeterReadings.txt")
    obj = ps.PowerService()
    obj.read_data(records)

    top = obj.find_top3_meters()
    print("Top 3 Meter Codes:")
    for k, v in top.items():
        print(f"{k} : {v}")

    reading_id = input("\nEnter the reading id to search: ")
    try:
        ut.validate_reading_id(reading_id)
        result = obj.search_reading(reading_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except pe.InvalidReadingIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start reading date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end reading date (DD/MM/YYYY): "))
    hc = obj.find_high_consumption(s, e)

    if not hc:
        print("No high consumption readings found in the specified date range")
        return

    print("Readings with units consumed > 300:")
    for k, v in hc.items():
        print(f"{k} : {v}")

    consumer_type = input("\nEnter the consumer type for fixed charge update: ")
    updated = obj.update_fixed_charge(consumer_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated reading details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
