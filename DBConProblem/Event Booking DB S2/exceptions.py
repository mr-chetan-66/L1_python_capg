### exceptions.py
### Custom Exception classes for the Event Booking Management System


class EventNotFoundException(Exception):
    """Raised when no event is found for the given ID,
    or when no upcoming events exist."""
    pass


class SeatNotAvailableException(Exception):
    """Raised when the requested number of tickets exceeds
    the available seats for the event."""
    pass


class EventExpiredException(Exception):
    """Raised when attempting to book tickets for an event
    whose date is in the past."""
    pass


class InvalidTicketCountException(Exception):
    """Raised when the number of tickets requested is less than 1."""
    pass
