### inventory_util.py
### Utility / helper functions for Inventory Management
### — urgency grouping, days since restock, display, log file writing

from datetime import datetime, date
from exceptions import OutOfStockException


# ----------------------------------------------------------------
# GROUPING — group products into urgency buckets
# NOTE: OutOfStockException is raised AFTER the dict is fully built
# so the caller must catch it and still use the dict it had built
# before the exception propagated
# ----------------------------------------------------------------
def group_products_by_urgency(product_list):
    # Urgency rules:
    #   Critical -> quantity_in_stock == 0
    #   Low      -> 0 < qty <= reorder_level // 2
    #   Moderate -> reorder_level // 2 < qty <= reorder_level
    grouped      = {}
    has_critical = False

    for p in product_list:
        qty     = p.get_quantity_in_stock()
        reorder = p.get_reorder_level()

        if qty == 0:
            urgency      = 'Critical'
            has_critical = True
        elif qty <= reorder // 2:
            urgency = 'Low'
        else:
            urgency = 'Moderate'

        if urgency not in grouped:
            grouped[urgency] = []
        grouped[urgency].append(p)

    # Raise AFTER building the full dict — caller is responsible for
    # rebuilding grouping if it needs the dict after catching this exception
    if has_critical:
        raise OutOfStockException(
            "Critical stock alert: one or more products are completely out of stock.")

    return grouped


# ----------------------------------------------------------------
# HELPER — build urgency grouping without raising (used by main
# after catching OutOfStockException to still display all groups)
# ----------------------------------------------------------------
def build_urgency_groups_silent(product_list):
    # Same logic as group_products_by_urgency but never raises
    # Used internally by main.py after OutOfStockException is caught
    grouped = {}
    for p in product_list:
        qty     = p.get_quantity_in_stock()
        reorder = p.get_reorder_level()

        if qty == 0:
            urgency = 'Critical'
        elif qty <= reorder // 2:
            urgency = 'Low'
        else:
            urgency = 'Moderate'

        if urgency not in grouped:
            grouped[urgency] = []
        grouped[urgency].append(p)

    return grouped


# ----------------------------------------------------------------
# CALCULATION — days elapsed since the product was last restocked
# ----------------------------------------------------------------
def calculate_days_since_restock(last_restocked_date):
    return (date.today() - last_restocked_date).days


# ----------------------------------------------------------------
# DISPLAY — print urgency-grouped low stock report to console
# ----------------------------------------------------------------
def display_low_stock_report(category, urgency_groups):
    print(f"\nLow Stock Report - Category: {category}")
    print("=" * 55)
    for urgency, products in urgency_groups.items():
        print(f"\n[{urgency}]")
        for p in products:
            days = calculate_days_since_restock(p.get_last_restocked_date())
            print(f"  Product ID        : {p.get_product_id()}")
            print(f"  Name              : {p.get_product_name()}")
            print(f"  Stock             : {p.get_quantity_in_stock()}")
            print(f"  Reorder Level     : {p.get_reorder_level()}")
            print(f"  Unit Price        : {p.get_unit_price()}")
            print(f"  Days Since Restock: {days}")
            print()


# ----------------------------------------------------------------
# FILE WRITE — append timestamped alert entries to log file
# Opens in 'a' mode — creates the file if it does not exist
# ----------------------------------------------------------------
def write_restock_log(product_list, log_filename):
    try:
        now = datetime.now().strftime("%d-%m-%Y %H:%M")
        with open(log_filename, 'a') as f:
            for p in product_list:
                days = calculate_days_since_restock(p.get_last_restocked_date())
                line = (
                    f"[{now}] ALERT: {p.get_product_name()} "
                    f"(ID: {p.get_product_id()}) | "
                    f"Stock: {p.get_quantity_in_stock()} | "
                    f"Reorder Level: {p.get_reorder_level()} | "
                    f"Days Since Restock: {days}\n"
                )
                f.write(line)

    except IOError as e:
        raise IOError(f"Failed to write log file: {e}")
