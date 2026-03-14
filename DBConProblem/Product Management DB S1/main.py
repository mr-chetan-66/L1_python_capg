### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import product_dao as dao
import product_util as util


def main():
    conn = db.get_connection()

    category  = input("Enter the category: ")
    threshold = int(input("Enter the stock threshold: "))

    if not util.is_valid_category(category):
        print("Invalid Category")
        return

    if not util.is_valid_threshold(threshold):
        print("Invalid Threshold")
        return

    result = dao.retrieve_low_stock_products(category, threshold, conn)

    if not result:
        print("No products found")
        return

    print("Total products found:", util.get_result_count(result))
    print("-" * 35)

    for product in result:
        util.display_product(product)
        days_left = util.get_days_until_expiry(product)
        print("Days Until Expiry    :", days_left)
        print("-" * 35)


if __name__ == '__main__':
    main()
