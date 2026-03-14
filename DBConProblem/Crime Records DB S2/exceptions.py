### exceptions.py
### Custom Exception classes for the Crime Record Management System


class InvalidLocationException(Exception):
    """Raised when no crime records are found for a given location,
    or when a crime record ID does not exist in the database."""
    pass


class InvalidCrimeTypeException(Exception):
    """Raised when an unknown crime type is encountered in records,
    or when an invalid status value is provided for a case update."""
    pass


class CaseAlreadyClosedException(Exception):
    """Raised when attempting to update the status of a case
    that is already marked as 'Closed'."""
    pass


class OfficerNotFoundException(Exception):
    """Raised when no officer record is found for the given officer ID."""
    pass
