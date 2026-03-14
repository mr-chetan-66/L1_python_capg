### exceptions.py
### Custom Exception classes for the Stock Portfolio Management System


class InvestorNotFoundException(Exception):
    """Raised when no portfolio exists for the given investor name,
    or when no holding exists for an investor in a specific symbol."""
    pass


class StockNotFoundException(Exception):
    """Raised when no stock record is found for the given ticker symbol."""
    pass


class InsufficientSharesException(Exception):
    """Raised when sell_quantity exceeds shares held,
    or when quantity < 1 or buy_price <= 0 during add_holding."""
    pass


class InvalidSectorException(Exception):
    """Raised when a stock's sector is not in VALID_SECTORS."""
    pass


class DuplicateHoldingException(Exception):
    """Raised when an investor already holds the specified stock symbol."""
    pass
