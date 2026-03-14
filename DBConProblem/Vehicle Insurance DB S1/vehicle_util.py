### vehicle_util.py
### Utility / helper functions for Vehicle — validation and display

from datetime import date

VALID_VEHICLE_TYPES = ['car', 'bike', 'truck', 'bus']


def is_valid_vehicle_type(vehicle_type):
    # Returns True if vehicle_type (case-insensitive) is in VALID_VEHICLE_TYPES
    return vehicle_type.lower() in VALID_VEHICLE_TYPES


def is_valid_renewal_date(new_expiry_date):
    # Returns True only if new_expiry_date is in the future (after today)
    return new_expiry_date > date.today()


def get_days_overdue(vehicle):
    # Returns number of days since insurance expired
    # insurance_expiry comes from Oracle as a Python datetime — extract .date()
    today   = date.today()
    expiry  = vehicle.get_insurance_expiry().date() \
              if hasattr(vehicle.get_insurance_expiry(), 'date') \
              else vehicle.get_insurance_expiry()
    return (today - expiry).days


def get_insurance_status(vehicle):
    # Returns 'Expired' if insurance_expiry < today, else 'Valid'
    today  = date.today()
    expiry = vehicle.get_insurance_expiry().date() \
             if hasattr(vehicle.get_insurance_expiry(), 'date') \
             else vehicle.get_insurance_expiry()
    if expiry < today:
        return "Expired"
    return "Valid"


def display_vehicle(vehicle):
    print("Vehicle ID         :", vehicle.get_vehicle_id())
    print("Owner Name         :", vehicle.get_owner_name())
    print("Vehicle Type       :", vehicle.get_vehicle_type())
    print("Brand              :", vehicle.get_brand())
    print("Model              :", vehicle.get_model())
    print("Registration Year  :", vehicle.get_registration_year())
    print("Insurance Expiry   :", vehicle.get_insurance_expiry())
    print("Insurance Status   :", get_insurance_status(vehicle))
    print("-" * 42)


def get_result_count(vehicle_list):
    return len(vehicle_list)


def get_most_overdue(vehicle_list):
    # Returns the Vehicle object with the oldest (most overdue) insurance expiry
    # Returns None if list is empty
    if not vehicle_list:
        return None
    return max(vehicle_list, key=lambda v: get_days_overdue(v))
