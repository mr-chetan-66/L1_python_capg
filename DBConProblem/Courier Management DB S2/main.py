### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import shipment_dao as dao_module
import courier_util as util
from exceptions import (ShipmentNotFoundException,
                        InvalidStatusTransitionException,
                        DeliveredShipmentException,
                        TrackingFileReadException)


def main():
    conn         = db.get_connection()
    shipment_dao = dao_module.ShipmentDao(conn)

    print("=" * 50)
    print("         COURIER TRACKING SYSTEM")
    print("=" * 50)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve shipment and display details + tracking history
    # ----------------------------------------------------------------
    print("\n--- RETRIEVE SHIPMENT ---")

    tracking_number = input("Enter Tracking Number : ")

    shipment_obj = shipment_dao.retrieve_shipment_by_tracking(tracking_number)
    history      = shipment_dao.retrieve_tracking_history(shipment_obj.get_shipment_id())
    metrics      = util.calculate_delivery_metrics(shipment_obj)

    print()
    util.display_shipment(shipment_obj, metrics)
    util.display_tracking_history(history)

    # ----------------------------------------------------------------
    # STEP 2 — Update shipment status via valid state-machine transition
    # ----------------------------------------------------------------
    print("\n--- UPDATE SHIPMENT STATUS ---")

    new_status  = input("Enter New Status      : ")
    location    = input("Enter Current Location: ")
    description = input("Enter Event Description: ")

    result = shipment_dao.update_shipment_status(
        tracking_number, new_status, location, description
    )
    print("Update Status :", result)

    # ----------------------------------------------------------------
    # STEP 3 — Bulk status update from CSV file
    # ----------------------------------------------------------------
    print("\n--- BULK STATUS UPDATE FROM FILE ---")

    bulk_file = input("Enter Bulk Update CSV File Path (or press Enter to skip) : ").strip()

    if bulk_file:
        bulk_results = util.load_bulk_status_updates_from_file(bulk_file, shipment_dao)
        print("\nBulk Update Results:")
        print("-" * 50)
        for trk, status, msg in bulk_results:
            print(f"  {trk} -> [{status}] {msg}")

    # ----------------------------------------------------------------
    # STEP 4 — Export full shipment report to text file
    # ----------------------------------------------------------------
    print("\n--- EXPORT SHIPMENT REPORT ---")

    filename = input("Enter Filename to Export Report : ")

    # Refresh tracking history to include any updates made above
    history = shipment_dao.retrieve_tracking_history(shipment_obj.get_shipment_id())

    util.export_shipment_report(shipment_obj, history, metrics, filename)
    print(f"Shipment report exported to {filename}")


if __name__ == '__main__':
    try:
        main()
    except ShipmentNotFoundException as e:
        print(e)
    except DeliveredShipmentException as e:
        print(e)
    except InvalidStatusTransitionException as e:
        print(e)
    except TrackingFileReadException as e:
        print(e)
    except ValueError:
        print("Invalid input.")
