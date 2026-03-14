### order_dao.py
### Data Access Object — contains all DB operations for Order
### Includes INSERT and SELECT functions

import order as od


def place_order(order_obj, conn):
    try:
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO orders (order_id, customer_name, product_id, quantity, order_date, status)
            VALUES (:1, :2, :3, :4, :5, :6)
        """

        cursor.execute(insert_query, (
            order_obj.get_order_id(),
            order_obj.get_customer_name(),
            order_obj.get_product_id(),
            order_obj.get_quantity(),
            order_obj.get_order_date(),
            order_obj.get_status()
        ))

        conn.commit()
        cursor.close()
        return True

    except Exception:
        return False


def retrieve_orders_by_customer(customer_name, conn):
    cursor = conn.cursor()

    query = """
        SELECT order_id, customer_name, product_id, quantity, order_date, status
        FROM orders
        WHERE LOWER(customer_name) = LOWER(:1)
        ORDER BY order_date DESC
    """

    cursor.execute(query, (customer_name,))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    order_list = []
    for row in rows:
        order_obj = od.Order(row[0], row[1], row[2], row[3], row[4], row[5])
        order_list.append(order_obj)

    return order_list
