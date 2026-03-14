### event_dao.py
### Data Access Object Class — all DB operations for Event and Booking
### Class-based DAO with SELECT (two tables), INSERT + UPDATE in single transaction

import event as ev
import booking as bk
import cx_Oracle
from datetime import datetime, date
from exceptions import (EventNotFoundException,
                        EventExpiredException,
                        SeatNotAvailableException,
                        InvalidTicketCountException)


class EventDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve a single event by event_id
    # ----------------------------------------------------------------
    def retrieve_event_by_id(self, event_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT event_id, event_name, venue, event_date, event_time,
                   total_seats, booked_seats, ticket_price
            FROM event
            WHERE event_id = :1
        """

        cursor.execute(query, (event_id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            raise EventNotFoundException("Event not found for the given ID.")

        return self.__map_row_to_event(row)

    # ----------------------------------------------------------------
    # SELECT — retrieve all upcoming events (event_date >= today)
    # ----------------------------------------------------------------
    def retrieve_upcoming_events(self):
        cursor = self.__conn.cursor()

        query = """
            SELECT event_id, event_name, venue, event_date, event_time,
                   total_seats, booked_seats, ticket_price
            FROM event
            WHERE event_date >= :1
            ORDER BY event_date ASC, event_time ASC
        """

        cursor.execute(query, (date.today(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise EventNotFoundException("No upcoming events available.")

        return [self.__map_row_to_event(row) for row in rows]

    # ----------------------------------------------------------------
    # INSERT + UPDATE — book tickets and update event seats atomically
    # ----------------------------------------------------------------
    def book_tickets(self, event_id, customer_name, num_tickets):
        # Step 1: Check if event exists — raises EventNotFoundException if not
        event_obj = self.retrieve_event_by_id(event_id)

        # Step 2: Check if event date is in the past
        if event_obj.get_event_date() < date.today():
            raise EventExpiredException(
                "Cannot book tickets for a past event.")

        # Step 3: Validate ticket count
        if num_tickets < 1:
            raise InvalidTicketCountException(
                "Number of tickets must be at least 1.")

        # Step 4: Check seat availability
        available = event_obj.get_total_seats() - event_obj.get_booked_seats()
        if available < num_tickets:
            raise SeatNotAvailableException(
                f"Not enough seats available. Only {available} seat(s) left.")

        try:
            booking_id   = event_id * 1000 + datetime.now().second
            total_amount = round(num_tickets * event_obj.get_ticket_price(), 2)
            today        = date.today()

            cursor = self.__conn.cursor()

            # INSERT new booking record
            insert_query = """
                INSERT INTO booking
                    (booking_id, event_id, customer_name,
                     num_tickets, booking_date, total_amount)
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            cursor.execute(insert_query, (
                booking_id, event_id, customer_name,
                num_tickets, today, total_amount
            ))

            # UPDATE event booked_seats in the same transaction
            update_query = """
                UPDATE event
                SET booked_seats = booked_seats + :1
                WHERE event_id = :2
            """
            cursor.execute(update_query, (num_tickets, event_id))

            self.__conn.commit()
            cursor.close()

            return bk.Booking(booking_id, event_id, customer_name,
                              num_tickets, today, total_amount)

        except (EventNotFoundException, EventExpiredException,
                InvalidTicketCountException, SeatNotAvailableException):
            raise
        except cx_Oracle.DatabaseError:
            self.__conn.rollback()
            raise

    # ----------------------------------------------------------------
    # PRIVATE — shared row-to-Event mapping used by both SELECT methods
    # ----------------------------------------------------------------
    def __map_row_to_event(self, row):
        # Safely handle Oracle DATE vs Python date
        e_date = row[3].date() if hasattr(row[3], 'date') else row[3]

        # Safely handle Oracle VARCHAR2 time string vs Python time object
        e_time = datetime.strptime(str(row[4]), "%H:%M").time() \
                 if not hasattr(row[4], 'hour') else row[4]

        return ev.Event(row[0], row[1], row[2], e_date, e_time,
                        row[5], row[6], float(row[7]))
