### rental_dao.py
### Data Access Object Class — all DB operations for Rental
### Class-based DAO with INSERT, SELECT, UPDATE, DELETE operations

import rental as rn
import cx_Oracle


class RentalDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve a single rental by rental_id
    # ----------------------------------------------------------------
    def retrieve_rental_by_id(self, rental_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT rental_id, customer_id, vehicle_id, start_date,
                   end_date, daily_rate, total_amount, payment_status
            FROM rental
            WHERE rental_id = :1
        """

        cursor.execute(query, (rental_id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return rn.Rental(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    # ----------------------------------------------------------------
    # INSERT — create a new rental with auto-calculated total_amount
    # ----------------------------------------------------------------
    def create_rental(self, rental_id, customer_id, vehicle_id,
                      start_date, end_date, daily_rate):
        try:
            # Calculate total amount from number of rental days
            num_days     = (end_date - start_date).days
            total_amount = round(num_days * daily_rate, 2)
            status       = 'Pending'

            cursor = self.__conn.cursor()

            insert_query = """
                INSERT INTO rental
                    (rental_id, customer_id, vehicle_id, start_date,
                     end_date, daily_rate, total_amount, payment_status)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """

            cursor.execute(insert_query, (
                rental_id, customer_id, vehicle_id,
                start_date, end_date, daily_rate,
                total_amount, status
            ))

            self.__conn.commit()
            cursor.close()

            # Return the full Rental object that was just created
            return rn.Rental(rental_id, customer_id, vehicle_id,
                             start_date, end_date, daily_rate,
                             total_amount, status)

        except cx_Oracle.DatabaseError:
            return None

    # ----------------------------------------------------------------
    # SELECT — retrieve all pending rentals for a customer
    # ----------------------------------------------------------------
    def retrieve_pending_rentals(self, customer_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT rental_id, customer_id, vehicle_id, start_date,
                   end_date, daily_rate, total_amount, payment_status
            FROM rental
            WHERE customer_id    = :1
              AND payment_status = 'Pending'
            ORDER BY start_date ASC
        """

        cursor.execute(query, (customer_id,))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return []

        rental_list = []
        for row in rows:
            rental_obj = rn.Rental(row[0], row[1], row[2], row[3],
                                   row[4], row[5], row[6], row[7])
            rental_list.append(rental_obj)

        return rental_list

    # ----------------------------------------------------------------
    # UPDATE — mark a rental as Paid
    # ----------------------------------------------------------------
    def mark_as_paid(self, rental_id):
        # Step 1: Check if rental exists
        rental = self.retrieve_rental_by_id(rental_id)

        if rental is None:
            return "Invalid Rental ID"

        # Step 2: Check if it is already paid
        if rental.get_payment_status() == 'Paid':
            return "Already Paid"

        # Step 3: Update status to 'Paid' and commit
        cursor = self.__conn.cursor()

        update_query = """
            UPDATE rental
            SET payment_status = 'Paid'
            WHERE rental_id = :1
        """

        cursor.execute(update_query, (rental_id,))
        self.__conn.commit()
        cursor.close()

        return "Payment Updated Successfully"

    # ----------------------------------------------------------------
    # DELETE — cancel (delete) a rental only if it is still Pending
    # ----------------------------------------------------------------
    def cancel_rental(self, rental_id):
        # Step 1: Check if rental exists
        rental = self.retrieve_rental_by_id(rental_id)

        if rental is None:
            return "Invalid Rental ID"

        # Step 2: Only Pending rentals can be cancelled
        if rental.get_payment_status() == 'Paid':
            return "Cannot Cancel Paid Rental"

        # Step 3: Delete the record and commit
        cursor = self.__conn.cursor()

        delete_query = """
            DELETE FROM rental
            WHERE rental_id = :1
        """

        cursor.execute(delete_query, (rental_id,))
        self.__conn.commit()
        cursor.close()

        return "Rental Cancelled Successfully"
