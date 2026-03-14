### crime_dao.py
### Data Access Object Class — all DB operations for CrimeRecord and Officer
### Class-based DAO with SELECT (two tables), UPDATE with commit/rollback

import crime_record as cr
import officer as of
import cx_Oracle
from exceptions import (InvalidLocationException,
                        InvalidCrimeTypeException,
                        CaseAlreadyClosedException,
                        OfficerNotFoundException)

# Valid statuses for a crime case
VALID_CASE_STATUSES = ['Open', 'Under Investigation', 'Closed']


class CrimeDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all crime records for a given location
    # ----------------------------------------------------------------
    def retrieve_crimes_by_location(self, location):
        cursor = self.__conn.cursor()

        query = """
            SELECT record_id, case_number, crime_type, location,
                   reported_date, status, officer_id, suspect_name
            FROM crime_record
            WHERE LOWER(location) = :1
            ORDER BY reported_date DESC
        """

        cursor.execute(query, (location.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise InvalidLocationException(
                "No crime records found for the given location.")

        crime_list = []
        for row in rows:
            # Safely handle Oracle datetime vs date
            r_date = row[4].date() if hasattr(row[4], 'date') else row[4]
            obj    = cr.CrimeRecord(row[0], row[1], row[2], row[3],
                                    r_date, row[5], row[6], row[7])
            crime_list.append(obj)

        return crime_list

    # ----------------------------------------------------------------
    # SELECT — retrieve a single officer record by officer_id
    # ----------------------------------------------------------------
    def retrieve_officer_details(self, officer_id):
        cursor = self.__conn.cursor()

        query = """
            SELECT officer_id, officer_name, badge_number,
                   rank, department, joining_date
            FROM officer
            WHERE officer_id = :1
        """

        cursor.execute(query, (officer_id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            raise OfficerNotFoundException(
                "Officer not found for the given ID.")

        # Safely handle Oracle datetime vs date
        j_date = row[5].date() if hasattr(row[5], 'date') else row[5]

        return of.Officer(row[0], row[1], row[2], row[3], row[4], j_date)

    # ----------------------------------------------------------------
    # UPDATE — update the status of a crime case with ordered validation
    # ----------------------------------------------------------------
    def update_case_status(self, record_id, new_status):
        try:
            cursor = self.__conn.cursor()

            # Step 1: Check if record exists
            cursor.execute(
                "SELECT status FROM crime_record WHERE record_id = :1",
                (record_id,)
            )
            row = cursor.fetchone()

            if row is None:
                cursor.close()
                raise InvalidLocationException(
                    "Crime record not found for the given ID.")

            # Step 2: Check if case is already closed
            current_status = row[0]
            if current_status == 'Closed':
                cursor.close()
                raise CaseAlreadyClosedException(
                    "Case is already closed and cannot be updated.")

            # Step 3: Validate the new status value
            if new_status not in VALID_CASE_STATUSES:
                cursor.close()
                raise InvalidCrimeTypeException(
                    "Invalid status. Must be Open, Under Investigation, or Closed.")

            # Step 4: Perform the UPDATE and commit
            update_query = """
                UPDATE crime_record
                SET status = :1
                WHERE record_id = :2
            """
            cursor.execute(update_query, (new_status, record_id))
            self.__conn.commit()
            cursor.close()

            return "Case status updated successfully."

        except (InvalidLocationException, CaseAlreadyClosedException,
                InvalidCrimeTypeException):
            raise
        except cx_Oracle.DatabaseError:
            self.__conn.rollback()
            raise
