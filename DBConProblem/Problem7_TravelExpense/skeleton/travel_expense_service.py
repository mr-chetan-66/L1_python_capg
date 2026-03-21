### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
# You can add any number of methods and attributes as required without changing the given template

import oracledb
import utility as ut
import exception as ex
import travel_expense as te

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class TravelExpenseService:

    def __init__(self):
        self.__travel_expense_list = []

    def get_travel_expense_details(self, input_file):
        """
        Call utility.read_file() with input_file.
        Pass the result to build_travel_expense_list().
        Return __travel_expense_list.
        """
        # Write your code here
        pass

    def build_travel_expense_list(self, records):
        """
        For each record string:
          1. Validate expense_id  -> catch InvalidExpenseIdException, print the message
          2. Validate city_tier   -> catch InvalidCityTierException, print the message
          3. Convert date strings using utility.convert_date()
          4. Create a TravelExpense object
          5. Call calculate_travel_costs() and set all cost attributes on the object
          6. Append the object to __travel_expense_list
        Returns None.
        """
        # Write your code here
        pass

    def calculate_travel_costs(self, no_of_days, city_tier, travel_mode):
        """
        Return [flight_or_transport_cost, hotel_cost, meal_cost,
                incidental_allowance, total_expense] as a list of floats.

        Step 1 – City-tier based daily rates (INR):
        +--------+----------------+----------+-----------+----------------------+
        | Tier   | Hotel / Day    | Meal/Day | Incid/Day | Notes                |
        +--------+----------------+----------+-----------+----------------------+
        | Tier1  |    5000        |  1200    |   500     | Metro cities         |
        | Tier2  |    2500        |   700    |   300     | State capitals       |
        | Tier3  |    1200        |   400    |   150     | Other cities         |
        +--------+----------------+----------+-----------+----------------------+

        hotel_cost           = hotel_rate_per_day   * no_of_days
        meal_cost            = meal_rate_per_day     * no_of_days
        incidental_allowance = incidental_rate_per_day * no_of_days

        Step 2 – Travel mode determines flight_or_transport_cost (flat amount, NOT per day):
        +-------------+---------------------------+
        | Travel Mode | Cost (INR, flat)           |
        +-------------+---------------------------+
        | Flight      | 8000  * city_tier_factor   |
        | Train       | 1500  * city_tier_factor   |
        | Bus         |  800  * city_tier_factor   |
        | Own Vehicle |  500  (fixed, no factor)   |
        +-------------+---------------------------+

        city_tier_factor:   Tier1 = 2.0,  Tier2 = 1.5,  Tier3 = 1.0

        For 'Own Vehicle', cost is always 500 regardless of city tier.

        Step 3:
        total_expense = flight_or_transport_cost + hotel_cost + meal_cost + incidental_allowance
        """
        # Write your code here
        pass

    def add_travel_expense_details(self, expense_list):
        """
        Insert each TravelExpense object in expense_list into the
        'travel_expense' table.
        Column order: expense_id, employee_id, date_of_travel, city_tier,
                      date_of_return, no_of_days, travel_mode, approval_status,
                      flight_or_transport_cost, hotel_cost, meal_cost,
                      incidental_allowance, total_expense
        Returns None.
        """
        # Write your code here
        pass

    def search_expense(self, expense_id):
        """
        Query 'travel_expense' by expense_id.
        If found, build and return a fully populated TravelExpense object.
        If not found, return None.
        """
        # Write your code here
        pass

    def update_meal_cost(self, no_of_days_threshold):
        """
        For all records in 'travel_expense' where no_of_days > no_of_days_threshold:
          - Increase meal_cost by 12%
          - Increase incidental_allowance by 12%
          - Recalculate total_expense = flight_or_transport_cost + hotel_cost
                                        + new_meal_cost + new_incidental_allowance
        Commit the update. Fetch and return all updated TravelExpense objects as a list.
        Return None if no records qualify.
        """
        # Write your code here
        pass
