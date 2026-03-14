### order_util.py
### Utility / helper functions for Order — validation and display

import order as od
from datetime import date

VALID_STATUSES = ['pending', 'shipped', 'delivered', 'cancelled']


def build_order(order_id, customer_name, product_id, quantity):
    # Creates and returns an Order object with today's date and 'Pending' status
    return od.Order(order_id, customer_name, product_id, quantity, date.today(), 'Pending')


def is_valid_quantity(quantity):
    # Returns True only if quantity is a positive integer
    return quantity > 0


def is_valid_status(status):
    # Returns True if status (case-insensitive) is in VALID_STATUSES
    return status.lower() in VALID_STATUSES


def display_order(order):
    print("Order ID      :", order.get_order_id())
    print("Customer Name :", order.get_customer_name())
    print("Product ID    :", order.get_product_id())
    print("Quantity      :", order.get_quantity())
    print("Order Date    :", order.get_order_date())
    print("Status        :", order.get_status())
    print("-" * 35)


def get_result_count(order_list):
    return len(order_list)


def get_total_quantity_ordered(order_list):
    # Returns the sum of quantities across all orders in the list
    return sum(o.get_quantity() for o in order_list)
