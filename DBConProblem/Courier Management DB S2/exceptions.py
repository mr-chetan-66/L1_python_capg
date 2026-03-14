### exceptions.py
### Custom Exception classes for the Courier Tracking System


class ShipmentNotFoundException(Exception):
    """Raised when a shipment cannot be found by its tracking number."""
    pass


class InvalidStatusTransitionException(Exception):
    """Raised when a status update violates the valid transition pipeline."""
    pass


class DeliveredShipmentException(Exception):
    """Raised when attempting to update a shipment that is already Delivered or Returned."""
    pass


class TrackingFileReadException(Exception):
    """Raised when the bulk update CSV file cannot be opened or read."""
    pass
