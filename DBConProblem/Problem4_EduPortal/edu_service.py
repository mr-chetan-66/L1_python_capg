# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import enrollment as en
from datetime import timedelta
import oracledb
import edu_exception as ee

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class EduService:

    def __init__(self):
        self.__scholarship_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line in records:
        #   1. Validate course_code — catch InvalidCourseCodeException and print message
        #   2. Validate enrollment_id — catch InvalidEnrollmentIdException and print message
        #   3. Convert start_date and registration_date using utility
        #   4. Create Enrollment object
        #   5. Call calculate_fee() — store scholarship in self.__scholarship_dict keyed by enrollment_id
        #   6. Call add_enrollment_details() to insert into DB
        # Truncate the Enrollment table at the start.
        # Return None.
        pass

    def add_enrollment_details(self, obj):
        # Write your code here
        # Insert the Enrollment object into the 'Enrollment' table.
        # Column order: enrollment_id, course_code, student_name, grade_level,
        #               duration_days, start_date, registration_date, course_name,
        #               base_fee, scholarship_amount, payable_fee
        # Return None.
        pass

    def find_top3_courses(self):
        # Write your code here
        # Count how many times each course_code appears in the Enrollment table.
        # Return dict {course_code: count} for top 3 distinct counts, sorted descending.
        # Include ALL course_codes whose count falls within top 3 distinct values (handle ties).
        pass

    def search_enrollment(self, enrollment_id):
        # Write your code here
        # Query Enrollment table for given enrollment_id.
        # Return fully populated Enrollment object, or None if not found.
        pass

    def find_completion_dates(self, start_date, end_date):
        # Write your code here
        # Find all enrollments where:
        #   - duration_days > 35
        #   - start_date is between start_date and end_date (inclusive)
        # Completion date = start_date + duration_days (timedelta)
        # Return {enrollment_id: completion_date}. Return empty dict if none found.
        pass

    def update_payable_fee(self, grade_level):
        # Write your code here
        # For all enrollments matching the given grade_level:
        #   UPDATE: scholarship_amount = scholarship_amount * 1.15
        #           payable_fee = base_fee - (scholarship_amount * 1.15)
        # After update, SELECT all enrollments with that grade_level.
        # Return list of Enrollment objects with updated values, or None if none found.
        pass
