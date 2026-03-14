### exceptions.py
### Custom Exception classes for the Inventory Restock Management System


class InvalidCategoryException(Exception):
    """Raised when no products exist for the given category,
    or when a product_id is not found during a restock operation."""
    pass


class OutOfStockException(Exception):
    """Raised when one or more products have quantity_in_stock == 0.
    Note: raised AFTER the urgency grouping dict is fully built."""
    pass


class RestockNotRequiredException(Exception):
    """Raised when the category exists in the DB but all its products
    are sufficiently stocked (none are at or below reorder level)."""
    pass
