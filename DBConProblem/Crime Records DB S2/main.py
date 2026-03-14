### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import crime_dao as dao_module
import crime_util as util
from exceptions import (InvalidLocationException,
                        InvalidCrimeTypeException,
                        CaseAlreadyClosedException,
                        OfficerNotFoundException)


def main():
    conn      = db.get_connection()
    crime_dao = dao_module.CrimeDao(conn)

    print("=" * 55)
    print("        CRIME RECORD MANAGEMENT SYSTEM")
    print("=" * 55)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve all crimes for a location and display grouped summary
    # ----------------------------------------------------------------
    print("\n--- RETRIEVE CRIMES BY LOCATION ---")

    location = input("Enter Location to Search : ")

    crimes = crime_dao.retrieve_crimes_by_location(location)

    try:
        grouped = util.group_crimes_by_type(crimes)
        util.display_crime_summary(location, grouped)
    except InvalidCrimeTypeException as e:
        print(e)

    # ----------------------------------------------------------------
    # STEP 2 — Update the status of a specific crime case
    # ----------------------------------------------------------------
    print("\n--- UPDATE CASE STATUS ---")

    record_id  = int(input("Enter Crime Record ID to Update : "))
    new_status = input("Enter New Status (Open / Under Investigation / Closed) : ")

    result = crime_dao.update_case_status(record_id, new_status)
    print("Update Status :", result)

    # ----------------------------------------------------------------
    # STEP 3 — Export full crime report with officer details to file
    # ----------------------------------------------------------------
    print("\n--- EXPORT CRIME REPORT ---")

    filename = input("Enter Filename to Export Report : ")

    util.export_crime_report(crimes, crime_dao, filename)
    print(f"Crime report exported to {filename}")


if __name__ == '__main__':
    try:
        main()
    except InvalidLocationException as e:
        print(e)
    except CaseAlreadyClosedException as e:
        print(e)
    except InvalidCrimeTypeException as e:
        print(e)
    except OfficerNotFoundException as e:
        print(e)
    except ValueError:
        print("Invalid input. Please enter valid values.")
