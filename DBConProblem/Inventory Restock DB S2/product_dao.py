### product_dao.py
### Data Access Object Class — all DB operations for Product
### Class-based DAO with SELECT (low stock) and UPDATE (restock)

import product as pr
import cx_Oracle
from datetime import date
from exceptions import InvalidCategoryException, RestockNotRequiredException


class ProductDao:

    def __init__(self, conn):
        self.__conn = conn

    # ----------------------------------------------------------------
    # SELECT — retrieve all low-stock products for a given category
    # Two-step query: first COUNT to distinguish "no category" vs
    # "category exists but all stocked"
    # ----------------------------------------------------------------
    def retrieve_low_stock_products(self, category):
        cursor = self.__conn.cursor()

        # Step 1: Check if the category exists at all
        check_query = """
            SELECT COUNT(*) FROM product
            WHERE LOWER(category) = :1
        """
        cursor.execute(check_query, (category.lower(),))
        total = cursor.fetchone()[0]

        if total == 0:
            cursor.close()
            raise InvalidCategoryException(
                "No products found for the given category.")

        # Step 2: Fetch only products at or below their reorder level
        query = """
            SELECT product_id, product_name, category, quantity_in_stock,
                   reorder_level, unit_price, last_restocked_date
            FROM product
            WHERE LOWER(category) = :1
              AND quantity_in_stock <= reorder_level
            ORDER BY quantity_in_stock ASC
        """
        cursor.execute(query, (category.lower(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            raise RestockNotRequiredException(
                "All products in this category are sufficiently stocked.")

        product_list = []
        for row in rows:
            # Safely handle Oracle datetime vs date
            restock_date = row[6].date() if hasattr(row[6], 'date') else row[6]
            obj = pr.Product(row[0], row[1], row[2], row[3], row[4],
                             float(row[5]), restock_date)
            product_list.append(obj)

        return product_list

    # ----------------------------------------------------------------
    # UPDATE — add stock quantity and refresh last_restocked_date
    # ----------------------------------------------------------------
    def restock_product(self, product_id, restock_quantity):
        try:
            cursor = self.__conn.cursor()

            # Step 1: Check if product exists
            cursor.execute(
                "SELECT COUNT(*) FROM product WHERE product_id = :1",
                (product_id,)
            )
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.close()
                raise InvalidCategoryException("Product ID not found.")

            # Step 2: UPDATE quantity and restock date, then commit
            update_query = """
                UPDATE product
                SET quantity_in_stock   = quantity_in_stock + :1,
                    last_restocked_date = :2
                WHERE product_id = :3
            """
            cursor.execute(update_query, (restock_quantity, date.today(), product_id))
            self.__conn.commit()
            cursor.close()

            return "Restock successful."

        except InvalidCategoryException:
            raise
        except cx_Oracle.DatabaseError:
            self.__conn.rollback()
            raise
