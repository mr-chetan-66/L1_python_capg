### subscription_util.py
### Utility / helper functions for Subscription — validation, display,
### expiry logic, grouping, status label and file export

from datetime import date

VALID_STATUSES = ['expired', 'expires today', 'expiring soon', 'active']


def is_valid_subscription_id(subscription_id):
    # Returns True only if subscription_id is a positive integer
    return subscription_id > 0


def is_valid_renewal_months(renewal_months):
    # Returns True only if renewal_months is between 1 and 12 inclusive
    return 1 <= renewal_months <= 12


def get_expiry_status(end_date):
    # Returns expiry status label based on days remaining until end_date
    days_remaining = (end_date - date.today()).days
    if days_remaining < 0:
        return 'Expired'
    elif days_remaining == 0:
        return 'Expires Today'
    elif days_remaining <= 7:
        return 'Expiring Soon'
    else:
        return 'Active'


def get_days_remaining(end_date):
    # Returns number of days remaining (negative if already expired)
    return (end_date - date.today()).days


def group_subscriptions_by_expiry_status(subscription_list):
    # Groups Subscription objects by their expiry status using get_expiry_status()
    # Returns dict with only keys that have at least one subscription
    grouped = {}
    for s in subscription_list:
        status = get_expiry_status(s.get_end_date())
        if status not in grouped:
            grouped[status] = []
        grouped[status].append(s)
    return grouped


def get_status_label(subscription):
    # Returns a formatted label based on expiry status
    status = get_expiry_status(subscription.get_end_date())
    if status == 'Active':
        return "✔ Active"
    elif status == 'Expiring Soon':
        return "⚠ Expiring Soon"
    elif status == 'Expires Today':
        return "⏰ Expires Today"
    return "✗ Expired"


def display_subscription(subscription):
    # Prints all subscription fields neatly with aligned labels
    print("Subscription ID :", subscription.get_subscription_id())
    print("Customer Name   :", subscription.get_customer_name())
    print("Email           :", subscription.get_email())
    print("Plan Type       :", subscription.get_plan_type())
    print("Start Date      :", subscription.get_start_date().strftime('%d-%m-%Y'))
    print("End Date        :", subscription.get_end_date().strftime('%d-%m-%Y'))
    print("Monthly Fee     : Rs.", subscription.get_monthly_fee())
    print("Active          :", "Yes" if subscription.get_is_active() == 1 else "No")
    print("Days Remaining  :", get_days_remaining(subscription.get_end_date()))
    print("Expiry Status   :", get_expiry_status(subscription.get_end_date()))
    print("-" * 42)


def get_result_count(subscription_list):
    # Returns total number of subscriptions in the list
    return len(subscription_list)


def get_active_count(subscription_list):
    # Returns count of subscriptions with expiry status 'Active'
    return sum(1 for s in subscription_list
               if get_expiry_status(s.get_end_date()) == 'Active')


def get_non_active_count(subscription_list):
    # Returns count of subscriptions that are NOT 'Active'
    return sum(1 for s in subscription_list
               if get_expiry_status(s.get_end_date()) != 'Active')


def export_expiry_alert_report(subscription_list, filename):
    # Writes only Expired / Expiring Soon / Expires Today subscriptions to file
    # Skips subscriptions with status 'Active'
    # Raises IOError if file cannot be written
    try:
        with open(filename, 'w') as f:
            f.write("SUBSCRIPTION EXPIRY ALERT REPORT\n")
            f.write("=" * 55 + "\n\n")

            written = 0
            for s in subscription_list:
                status = get_expiry_status(s.get_end_date())
                if status == 'Active':
                    continue

                days = get_days_remaining(s.get_end_date())
                f.write(f"Subscription ID : {s.get_subscription_id()}\n")
                f.write(f"Customer        : {s.get_customer_name()}\n")
                f.write(f"Email           : {s.get_email()}\n")
                f.write(f"Plan            : {s.get_plan_type()}\n")
                f.write(f"End Date        : {s.get_end_date().strftime('%d-%m-%Y')}\n")
                f.write(f"Status          : {status}\n")
                f.write(f"Days Remaining  : {days}\n")
                f.write("-" * 55 + "\n")
                written += 1

            if written == 0:
                f.write("No subscriptions requiring alerts.\n")

    except IOError as e:
        raise IOError(f"Failed to write report: {e}")
