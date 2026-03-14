### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import order_dao as dao
import order_util as util
from datetime import date


def main():
    conn = db.get_connection()

    print("=" * 35)
    print("       PLACE A NEW ORDER")
    print("=" * 35)

    order_id      = int(input("Enter Order ID       : "))
    customer_name = input("Enter Customer Name  : ")
    product_id    = int(input("Enter Product ID     : "))
    quantity      = int(input("Enter Quantity       : "))

    if not util.is_valid_quantity(quantity):
        print("Invalid Quantity")
        return

    # Order is always placed with today's date and 'Pending' status
    new_order = util.build_order(order_id, customer_name, product_id, quantity)

    success = dao.place_order(new_order, conn)

    if not success:
        print("Order Placement Failed")
        return

    print("\nOrder Placed Successfully!")

    # Show full order history for this customer
    print("\n" + "=" * 35)
    print(f"  ORDER HISTORY — {customer_name.upper()}")
    print("=" * 35)

    orders = dao.retrieve_orders_by_customer(customer_name, conn)

    if not orders:
        print("No orders found")
        return

    print("Total Orders        :", util.get_result_count(orders))
    print("Total Items Ordered :", util.get_total_quantity_ordered(orders))
    print("-" * 35)

    for order in orders:
        util.display_order(order)


if __name__ == '__main__':
    main()
