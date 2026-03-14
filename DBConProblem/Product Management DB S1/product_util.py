### product_util.py
### Utility / helper functions for Product — validation and display

from datetime import date

VALID_CATEGORIES = ['dairy', 'bakery', 'beverages', 'snacks', 'frozen', 'meat', 'produce']


def is_valid_category(category):
    # Returns True if category (case-insensitive) is in VALID_CATEGORIES
    return category.lower() in VALID_CATEGORIES


def is_valid_threshold(threshold):
    # Returns True if threshold is a positive integer
    return threshold > 0


def display_product(product):
    print("Product ID   :", product.get_product_id())
    print("Product Name :", product.get_product_name())
    print("Category     :", product.get_category())
    print("Price        :", product.get_price())
    print("Stock        :", product.get_stock_quantity())
    print("Expiry Date  :", product.get_expiry_date())
    print("-" * 35)


def get_result_count(product_list):
    return len(product_list)


def get_days_until_expiry(product):
    # Returns number of days remaining until the product expires
    # expiry_date comes back from Oracle as a Python datetime object
    today = date.today()
    expiry = product.get_expiry_date().date() if hasattr(product.get_expiry_date(), 'date') else product.get_expiry_date()
    return (expiry - today).days
