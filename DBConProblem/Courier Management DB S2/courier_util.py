### courier_util.py
### Utility / helper functions for Courier — metrics, display, file operations

from datetime import date
from exceptions import TrackingFileReadException


# ----------------------------------------------------------------
# METRICS — calculate delivery timing and shipping cost
# ----------------------------------------------------------------
def calculate_delivery_metrics(shipment_obj):
    # days from dispatch date to today
    today           = date.today()
    days_in_transit = (today - shipment_obj.get_dispatch_date()).days

    # days from today to expected delivery (negative means overdue)
    days_until_due  = (shipment_obj.get_expected_delivery_date() - today).days

    # overdue only if past due AND not yet in a terminal status
    is_overdue      = (days_until_due < 0 and
                       shipment_obj.get_status() not in ['Delivered', 'Returned'])

    # tiered shipping cost based on weight
    weight = shipment_obj.get_weight_kg()
    if weight <= 5:
        shipping_cost = round(weight * 50.0, 2)
    elif weight <= 20:
        shipping_cost = round(weight * 40.0, 2)
    else:
        shipping_cost = round(weight * 30.0, 2)

    return {
        'days_in_transit' : days_in_transit,
        'days_until_due'  : days_until_due,
        'is_overdue'      : is_overdue,
        'shipping_cost'   : shipping_cost
    }


# ----------------------------------------------------------------
# DISPLAY — print shipment details and tracking history to console
# ----------------------------------------------------------------
def display_shipment(shipment_obj, metrics):
    print(f"Shipment Found : {shipment_obj.get_tracking_number()}")
    print(f"Status         : {shipment_obj.get_status()}")
    print(f"Route          : {shipment_obj.get_origin_city()} -> {shipment_obj.get_destination_city()}")
    print(f"Sender         : {shipment_obj.get_sender_name()}")
    print(f"Receiver       : {shipment_obj.get_receiver_name()}")
    print(f"Weight         : {shipment_obj.get_weight_kg()} kg")
    print(f"Days In Transit: {metrics['days_in_transit']}")
    print(f"Days Until Due : {metrics['days_until_due']}")
    print(f"Overdue        : {'Yes' if metrics['is_overdue'] else 'No'}")
    print(f"Shipping Cost  : Rs. {metrics['shipping_cost']}")
    print("-" * 50)


def display_tracking_history(tracking_history):
    print("\nTracking History:")
    if not tracking_history:
        print("  No events recorded yet.")
    else:
        for event in tracking_history:
            print(f"  {event.get_event_datetime().strftime('%d-%m-%Y %H:%M')}  "
                  f"[{event.get_location()}]  {event.get_event_description()}")


# ----------------------------------------------------------------
# FILE READ — load bulk status updates from CSV and apply each one
# shipment_dao object is passed in so this function stays DB-free
# ----------------------------------------------------------------
def load_bulk_status_updates_from_file(filepath, shipment_dao):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except IOError:
        raise TrackingFileReadException(f"Could not read update file: {filepath}")

    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',', 3)
        if len(parts) < 4:
            results.append((line, 'FAILED', 'Malformed line — expected 4 fields.'))
            continue

        tracking_number, new_status, location, description = [p.strip() for p in parts]

        try:
            msg = shipment_dao.update_shipment_status(
                tracking_number, new_status, location, description
            )
            results.append((tracking_number, 'SUCCESS', msg))
        except Exception as e:
            results.append((tracking_number, 'FAILED', str(e)))

    return results


# ----------------------------------------------------------------
# FILE WRITE — export full shipment report to a text file
# ----------------------------------------------------------------
def export_shipment_report(shipment_obj, tracking_history, metrics, filename):
    try:
        with open(filename, 'w') as f:
            f.write("============ SHIPMENT TRACKING REPORT ============\n")
            f.write(f"Tracking No       : {shipment_obj.get_tracking_number()}\n")
            f.write(f"Sender            : {shipment_obj.get_sender_name()}\n")
            f.write(f"Receiver          : {shipment_obj.get_receiver_name()}\n")
            f.write(f"Route             : {shipment_obj.get_origin_city()} -> {shipment_obj.get_destination_city()}\n")
            f.write(f"Dispatch Date     : {shipment_obj.get_dispatch_date().strftime('%d-%m-%Y')}\n")
            f.write(f"Expected Delivery : {shipment_obj.get_expected_delivery_date().strftime('%d-%m-%Y')}\n")
            f.write(f"Weight            : {shipment_obj.get_weight_kg()} kg\n")
            f.write(f"Shipping Cost     : Rs. {metrics['shipping_cost']}\n")
            f.write(f"Current Status    : {shipment_obj.get_status()}\n")
            f.write(f"Days In Transit   : {metrics['days_in_transit']}\n")
            f.write(f"Days Until Due    : {metrics['days_until_due']}  (negative = overdue)\n")
            f.write(f"Overdue           : {'Yes' if metrics['is_overdue'] else 'No'}\n")
            f.write("-" * 50 + "\n")
            f.write("TRACKING HISTORY:\n")

            if not tracking_history:
                f.write("  (No events recorded yet.)\n")
            else:
                for event in tracking_history:
                    f.write(
                        f"  {event.get_event_datetime().strftime('%d-%m-%Y %H:%M')}  "
                        f"[{event.get_location()}]  {event.get_event_description()}\n"
                    )

            f.write("=" * 50 + "\n")

    except IOError as e:
        raise IOError(f"Failed to write report: {e}")
