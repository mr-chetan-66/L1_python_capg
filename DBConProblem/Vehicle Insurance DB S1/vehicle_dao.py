### vehicle_dao.py
### Data Access Object — contains all DB operations for Vehicle
### Includes SELECT by ID, expired insurance filter, and UPDATE insurance renewal

import vehicle as vh


def retrieve_vehicle_by_id(vehicle_id, conn):
    cursor = conn.cursor()

    query = """
        SELECT vehicle_id, owner_name, vehicle_type, brand, model,
               registration_year, insurance_expiry
        FROM vehicle
        WHERE vehicle_id = :1
    """

    cursor.execute(query, (vehicle_id,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return vh.Vehicle(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


def retrieve_expired_insurance_vehicles(vehicle_type, conn):
    cursor = conn.cursor()

    query = """
        SELECT vehicle_id, owner_name, vehicle_type, brand, model,
               registration_year, insurance_expiry
        FROM vehicle
        WHERE LOWER(vehicle_type) = LOWER(:1)
          AND insurance_expiry < SYSDATE
        ORDER BY insurance_expiry ASC
    """

    cursor.execute(query, (vehicle_type,))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    vehicle_list = []
    for row in rows:
        vehicle_obj = vh.Vehicle(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        vehicle_list.append(vehicle_obj)

    return vehicle_list


def renew_insurance(vehicle_id, new_expiry_date, conn):
    # Step 1: Check if vehicle exists
    vehicle = retrieve_vehicle_by_id(vehicle_id, conn)

    if vehicle is None:
        return "Invalid Vehicle ID"

    # Step 2: Update insurance_expiry to new_expiry_date and commit
    cursor = conn.cursor()

    update_query = """
        UPDATE vehicle
        SET insurance_expiry = :1
        WHERE vehicle_id = :2
    """

    cursor.execute(update_query, (new_expiry_date, vehicle_id))
    conn.commit()
    cursor.close()

    return "Insurance Renewed Successfully"
