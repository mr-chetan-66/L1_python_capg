### shipment_dao.py
### Data Access Object Class — all DB operations for Shipment and TrackingEvent
### Class-based DAO with SELECT, INSERT + UPDATE in single transaction

import shipment as sh
import tracking_event as te
import cx_Oracle
from datetime import datetime
from exceptions import (ShipmentNotFoundException,
                        InvalidStatusTransitionException,
                        DeliveredShipmentException)

# Define valid status pipeline (order matters)
STATUS_PIPELINE = ['Booked', 'In Transit', 'Out for Delivery', 'Delivered', 'Returned']

# Valid forward transitions
# A shipment can only move forward in the pipeline
# except 'Returned' which can come from 'In Transit' or 'Out for Delivery'
VALID_TRANSITIONS = {
    'Booked'           : ['In Transit'],
    'In Transit'       : ['Out for Delivery', 'Returned'],
    'Out for Delivery' : ['Delivered', 'Returned'],
    'Delivered'        : [],
    'Returned'         : []
}


class ShipmentDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve a single shipment by tracking number
    # ----------------------------------------------------------------
    def retrieve_shipment_by_tracking(self, tracking_number):
        cursor = self.__conn.cursor()

        query = """
            SELECT shipment_id, tracking_number, sender_name, receiver_name,
                   origin_city, destination_city, dispatch_date,
                   expected_delivery_date, weight_kg, status
            FROM shipment
            WHERE tracking_number = :1
        """

        cursor.execute(query, (tracking_number,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            raise ShipmentNotFoundException(
                f"No shipment found for tracking number: {tracking_number}")

        # Safely handle Oracle datetime vs date
        dispatch_date          = row[6].date() if hasattr(row[6], 'date') else row[6]
        expected_delivery_date = row[7].date() if hasattr(row[7], 'date') else row[7]

        return sh.Shipment(row[0], row[1], row[2], row[3], row[4],
                           row[5], dispatch_date, expected_delivery_date,
                           float(row[8]), row[9])

    # ----------------------------------------------------------------
    # SELECT — retrieve all tracking events for a shipment
    # ----------------------------------------------------------------
    def retrieve_tracking_history(self, shipment_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT event_id, shipment_id, event_datetime, location, event_description
            FROM tracking_event
            WHERE shipment_id = :1
            ORDER BY event_datetime ASC
        """

        cursor.execute(query, (shipment_id,))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return []

        event_list = []
        for row in rows:
            # Safely handle Oracle TIMESTAMP vs datetime
            evt_dt = row[2] if isinstance(row[2], datetime) \
                     else datetime.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S")

            event_obj = te.TrackingEvent(row[0], row[1], evt_dt, row[3], row[4])
            event_list.append(event_obj)

        return event_list

    # ----------------------------------------------------------------
    # UPDATE + INSERT — update shipment status and log tracking event
    # Both operations committed in a single transaction
    # ----------------------------------------------------------------
    def update_shipment_status(self, tracking_number, new_status, location, description):
        # Step 1: Check if shipment exists — raises ShipmentNotFoundException if not
        shipment_obj   = self.retrieve_shipment_by_tracking(tracking_number)
        current_status = shipment_obj.get_status()

        # Step 2: Block updates on terminal statuses
        if current_status in ['Delivered', 'Returned']:
            raise DeliveredShipmentException(
                f"Shipment is already {current_status} and cannot be updated.")

        # Step 3: Validate the status transition against the pipeline
        if new_status not in VALID_TRANSITIONS.get(current_status, []):
            raise InvalidStatusTransitionException(
                f"Invalid transition: {current_status} -> {new_status}")

        try:
            cursor      = self.__conn.cursor()
            shipment_id = shipment_obj.get_shipment_id()
            event_id    = shipment_id * 100 + datetime.now().second
            now         = datetime.now()

            # UPDATE shipment status
            update_query = """
                UPDATE shipment
                SET status = :1
                WHERE tracking_number = :2
            """
            cursor.execute(update_query, (new_status, tracking_number))

            # INSERT new tracking event in the same transaction
            insert_query = """
                INSERT INTO tracking_event
                    (event_id, shipment_id, event_datetime, location, event_description)
                VALUES (:1, :2, :3, :4, :5)
            """
            cursor.execute(insert_query, (
                event_id, shipment_id, now, location, description
            ))

            self.__conn.commit()
            cursor.close()

            return f"Status updated to {new_status}."

        except cx_Oracle.DatabaseError:
            self.__conn.rollback()
            raise
