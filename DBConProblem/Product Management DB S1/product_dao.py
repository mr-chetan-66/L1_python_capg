### product_dao.py
### Data Access Object — contains all DB query functions for Product

import product as pr


def retrieve_low_stock_products(category, threshold, conn):
    cursor = conn.cursor()

    query = """
        SELECT product_id, product_name, category, price, stock_quantity, expiry_date
        FROM product
        WHERE LOWER(category) = LOWER(:1)
          AND stock_quantity <= :2
          AND expiry_date > SYSDATE
        ORDER BY stock_quantity ASC
    """

    cursor.execute(query, (category, threshold))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    product_list = []
    for row in rows:
        product_obj = pr.Product(row[0], row[1], row[2], row[3], row[4], row[5])
        product_list.append(product_obj)

    return product_list
