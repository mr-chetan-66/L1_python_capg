### rental_util.py
### Utility / helper functions for Rental — validation, display and calculations

from datetime import date

VALID_PAYMENT_STATUSES = ['pending', 'paid']


def is_valid_date_range(start_date, end_date):
    # Returns True only if end_date is strictly after start_date
    return end_date > start_date


def is_valid_daily_rate(daily_rate):
    # Returns True only if daily_rate is a positive number
    return daily_rate > 0


def is_valid_rental_id(rental_id):
    # Returns True only if rental_id is a positive integer
    return rental_id > 0


def calculate_rental_days(rental):
    # Returns number of days for the rental duration
    start = rental.get_start_date().date() \
            if hasattr(rental.get_start_date(), 'date') \
            else rental.get_start_date()
    end   = rental.get_end_date().date() \
            if hasattr(rental.get_end_date(), 'date') \
            else rental.get_end_date()
    return (end - start).days


def display_rental(rental):
    print("Rental ID      :", rental.get_rental_id())
    print("Customer ID    :", rental.get_customer_id())
    print("Vehicle ID     :", rental.get_vehicle_id())
    print("Start Date     :", rental.get_start_date())
    print("End Date       :", rental.get_end_date())
    print("Rental Days    :", calculate_rental_days(rental))
    print("Daily Rate     :", rental.get_daily_rate())
    print("Total Amount   :", rental.get_total_amount())
    print("Payment Status :", rental.get_payment_status())
    print("-" * 42)


def get_result_count(rental_list):
    return len(rental_list)


def get_total_pending_amount(rental_list):
    # Returns sum of total_amount for all rentals in the list
    return round(sum(r.get_total_amount() for r in rental_list), 2)


def get_longest_rental(rental_list):
    # Returns the Rental object with the most number of rental days
    # Returns None if list is empty
    if not rental_list:
        return None
    return max(rental_list, key=lambda r: calculate_rental_days(r))


def get_payment_status_label(rental):
    # Returns a formatted label based on payment status
    status = rental.get_payment_status()
    if status == 'Paid':
        return "✔ Paid"
    return "⏳ Pending"
