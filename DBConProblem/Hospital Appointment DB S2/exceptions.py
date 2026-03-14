### exceptions.py
### Custom Exception classes for the Hospital Appointment Management System


class InvalidDoctorException(Exception):
    """Raised when no appointments are found for the given doctor name."""
    pass


class InvalidStatusException(Exception):
    """Raised when any appointment in the list has a status outside
    the valid set: 'Scheduled', 'Completed', 'Cancelled'."""
    pass


class AppointmentSlotConflictException(Exception):
    """Raised when a 'Scheduled' appointment already exists for the
    given doctor at the specified date and time."""
    pass
