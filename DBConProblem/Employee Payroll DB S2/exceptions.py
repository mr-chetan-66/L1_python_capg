### exceptions.py
### Custom Exception classes for the Employee Payroll Management System


class InvalidDepartmentException(Exception):
    """Raised when no employees are found for the given department."""
    pass


class InsufficientExperienceException(Exception):
    """Raised when an employee has less than 1 complete year of experience."""
    pass
