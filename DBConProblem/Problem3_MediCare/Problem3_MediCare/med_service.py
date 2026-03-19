# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import medicine as md
from datetime import timedelta
import oracledb
import med_exception as me

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class MedService:

    def __init__(self):
        self.__margin_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line in records:
        #   1. Validate med_code — catch InvalidMedCodeException and print message
        #   2. Validate stock_id — catch InvalidStockIdException and print message
        #   3. Convert manufacture_date and expiry_date using utility
        #   4. Create Medicine object
        #   5. Call calculate_selling_price() — store margin in self.__margin_dict
        #   6. Call add_medicine_details() to insert into DB
        # Truncate the Medicine table at the start.
        # Return None.
        pass

    def add_medicine_details(self, obj):
        # Write your code here
        # Insert the Medicine object into the 'Medicine' table.
        # Column order: stock_id, med_code, med_name, category, unit_price, quantity,
        #               manufacture_date, expiry_date, margin_amount, selling_price, total_stock_value
        # Return None.
        pass

    def find_top3_medicines(self):
        # Write your code here
        # Count how many times each med_code appears in the Medicine table.
        # Return dict {med_code: count} of top 3 distinct counts, sorted descending.
        # Include ALL med_codes whose count ties within the top 3 distinct values.
        pass

    def search_stock(self, stock_id):
        # Write your code here
        # Query Medicine table for the given stock_id.
        # Return a fully populated Medicine object, or None if not found.
        pass

    def find_near_expiry(self, ref_date, days_threshold):
        # Write your code here
        # Find all medicines where:
        #   - quantity > 100
        #   - expiry_date is between ref_date and (ref_date + days_threshold) inclusive
        # Return dict {stock_id: expiry_date}. Return empty dict if none.
        pass

    def update_unit_price(self, category):
        # Write your code here
        # For all medicines matching the given category:
        #   UPDATE: unit_price = unit_price * 1.08
        #           margin_amount = unit_price * 1.08 * margin_rate  (recalculate from new unit_price)
        #           selling_price = unit_price * 1.08 + margin_amount
        #           total_stock_value = selling_price * quantity
        # Hint: It is acceptable to update unit_price, then recompute margin/selling/total in SQL.
        #       Use the same margin rates as in the Medicine model class.
        # After update, SELECT all medicines with that category.
        # Return list of Medicine objects with updated values, or None if none found.
        pass
