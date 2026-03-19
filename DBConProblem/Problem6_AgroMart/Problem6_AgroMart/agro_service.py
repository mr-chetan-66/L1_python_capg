# Please do not change the skeleton code given here.
# You can add any number of methods and attributes as required without changing the given template
import utility as ut
import crop as cr
from datetime import timedelta
import oracledb
import agro_exception as ae

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class AgroService:

    def __init__(self):
        self.__premium_dict = {}

    def read_data(self, records):
        # Write your code here
        # For each line in records:
        #   1. Validate crop_code — catch InvalidCropCodeException and print message
        #   2. Validate agri_id — catch InvalidAgriIdException and print message
        #   3. Convert harvest_date and listing_date using utility
        #   4. Create Crop object
        #   5. Call calculate_selling_price() — store premium in self.__premium_dict keyed by agri_id
        #   6. Call add_crop_details() to insert into DB
        # Truncate the Crop table at the start.
        # Return None.
        pass

    def add_crop_details(self, obj):
        # Write your code here
        # Insert Crop object into the 'Crop' table.
        # Column order: agri_id, crop_code, crop_name, crop_type, base_price,
        #               quantity_kg, season, harvest_date, listing_date,
        #               seasonal_premium, selling_price, total_value
        # Return None.
        pass

    def find_top3_crops(self):
        # Write your code here
        # Count how many times each crop_code appears in the Crop table.
        # Return {crop_code: count} for top 3 distinct counts, sorted descending.
        # Handle ties — all crop_codes within top 3 distinct values must be included.
        pass

    def search_crop(self, agri_id):
        # Write your code here
        # Query Crop table for given agri_id.
        # Return fully populated Crop object, or None if not found.
        pass

    def find_bulk_stock(self, start_date, end_date):
        # Write your code here
        # Find all crops where:
        #   - quantity_kg > 4000
        #   - harvest_date is between start_date and end_date (inclusive)
        # Return {agri_id: quantity_kg}. Return empty dict if none found.
        pass

    def update_base_price(self, season):
        # Write your code here
        # For all crops matching the given season:
        #   UPDATE: base_price = base_price * 1.12
        #           seasonal_premium = base_price * 1.12 * <season_rate>
        #           selling_price = base_price * 1.12 + seasonal_premium
        #           total_value = selling_price * quantity_kg
        # Use same season rates as calculate_selling_price.
        # After update, SELECT all crops with that season.
        # Return list of Crop objects with updated values, or None if none found.
        pass
