### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import scholarship_application as sa

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class ScholarshipService:

    def __init__(self):
        self.__scholarship_list = []

    def get_scholarship_details(self, input_file):
        """
        Call utility.read_file() with input_file.
        Pass the result to build_scholarship_list().
        Return __scholarship_list.
        """
        # Write your code here
        pass

    def build_scholarship_list(self, records):
        """
        For each record string:
          1. Validate application_id -> catch InvalidApplicationIdException, print message
          2. Validate course_type    -> catch InvalidCourseTypeException, print message
          3. Convert date strings using utility.convert_date()
          4. Create a ScholarshipApplication object
          5. Call calculate_scholarship() and set all calculated attributes on the object
          6. Append the object to __scholarship_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_scholarship(self, course_type, cgpa, annual_family_income, category):
        """
        Return [base_scholarship, merit_bonus, income_waiver, total_scholarship]
        as a list of floats.

        Step 1 – Base scholarship by course_type (INR per year):
        +----------+--------------------+
        | Course   | Base Scholarship   |
        +----------+--------------------+
        | UG       |    40,000          |
        | PG       |    60,000          |
        | Diploma  |    25,000          |
        | PhD      |   100,000          |
        +----------+--------------------+

        Step 2 – Merit bonus (% of base_scholarship) based on CGPA:
        +----------------+------------------+
        | CGPA Band      | Merit Bonus %    |
        +----------------+------------------+
        | 9.0 and above  |      25%         |
        | 8.0 – 8.99     |      15%         |
        | 7.0 – 7.99     |       8%         |
        | 6.0 – 6.99     |       0%         |
        +----------------+------------------+
        merit_bonus = base_scholarship * merit_bonus_pct / 100

        Step 3 – Income waiver (flat INR amount) based on annual_family_income:
        +------------------------------+------------------+
        | Annual Family Income (INR)   | Income Waiver    |
        +------------------------------+------------------+
        | Below 1,00,000               |    15,000        |
        | 1,00,000 – 2,49,999          |     8,000        |
        | 2,50,000 – 4,99,999          |     3,000        |
        | 5,00,000 and above           |         0        |
        +------------------------------+------------------+

        Step 4 – Category bonus applied to total_scholarship:
        After computing total_scholarship = base_scholarship + merit_bonus + income_waiver,
        apply the following category multiplier:
        +----------+------------+
        | Category | Multiplier |
        +----------+------------+
        | SC       |   1.20     |
        | ST       |   1.25     |
        | OBC      |   1.10     |
        | General  |   1.00     |
        +----------+------------+
        total_scholarship = (base_scholarship + merit_bonus + income_waiver) * multiplier
        Round total_scholarship to 2 decimal places.
        """
        # Write your code here
        pass

    def add_scholarship_details(self, scholarship_list):
        """
        Insert each ScholarshipApplication object in scholarship_list into
        the 'scholarship_application' table.
        Column order: application_id, student_id, date_of_application, course_type,
                      date_of_enrollment, cgpa, annual_family_income, category,
                      application_status, base_scholarship, merit_bonus,
                      income_waiver, total_scholarship
        Returns None.
        """
        # Write your code here
        pass

    def search_application(self, application_id):
        """
        Query 'scholarship_application' by application_id.
        If found, build and return a fully populated ScholarshipApplication object.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_merit_bonus(self, cgpa_threshold):
        """
        For all records in 'scholarship_application' where cgpa > cgpa_threshold:
          - Increase merit_bonus by 10% (multiply by 1.10)
          - Recalculate total_scholarship = base_scholarship + new_merit_bonus
                                            + income_waiver
            Note: do NOT re-apply the category multiplier during update —
            total_scholarship is simply the sum of the three components.
          - Update merit_bonus and total_scholarship columns in the database
        Commit the update. Fetch and return all updated ScholarshipApplication
        objects as a list.
        Return None if no records qualify.
        """
        # Write your code here
        pass
