### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import product_dao as dao_module
import inventory_util as util
from exceptions import (InvalidCategoryException,
                        OutOfStockException,
                        RestockNotRequiredException)


def main():
    conn        = db.get_connection()
    product_dao = dao_module.ProductDao(conn)

    print("=" * 55)
    print("       INVENTORY RESTOCK MANAGEMENT SYSTEM")
    print("=" * 55)

    # ----------------------------------------------------------------
    # STEP 1 — Retrieve low stock products and display urgency report
    # ----------------------------------------------------------------
    print("\n--- LOW STOCK REPORT ---")

    category          = input("Enter Product Category : ")
    low_stock_products = product_dao.retrieve_low_stock_products(category)

    # group_products_by_urgency raises OutOfStockException AFTER building
    # the full dict — catch it, print the warning, then rebuild the groups
    # silently so the report can still be displayed in full
    urgency_groups = {}
    try:
        urgency_groups = util.group_products_by_urgency(low_stock_products)
    except OutOfStockException as e:
        print(f"Warning: {e}")
        urgency_groups = util.build_urgency_groups_silent(low_stock_products)

    util.display_low_stock_report(category, urgency_groups)

    # ----------------------------------------------------------------
    # STEP 2 — Append timestamped alert entries to a log file
    # ----------------------------------------------------------------
    print("\n--- WRITE RESTOCK LOG ---")

    log_file = input("Enter Log Filename to Write Restock Alerts : ")

    util.write_restock_log(low_stock_products, log_file)
    print(f"Restock log written to {log_file}")

    # ----------------------------------------------------------------
    # STEP 3 — Restock a product by updating its stock and restock date
    # ----------------------------------------------------------------
    print("\n--- RESTOCK A PRODUCT ---")

    product_id  = input("Enter Product ID to Restock   : ")
    restock_qty = int(input("Enter Quantity to Add          : "))

    result = product_dao.restock_product(product_id, restock_qty)
    print(result)


if __name__ == '__main__':
    try:
        main()
    except InvalidCategoryException as e:
        print(e)
    except RestockNotRequiredException as e:
        print(e)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
