### crime_util.py
### Utility / helper functions for Crime Management — calculations, display, grouping, file export

from datetime import date
from exceptions import InvalidCrimeTypeException, OfficerNotFoundException

# Valid crime types — used for grouping validation
VALID_CRIME_TYPES = ['theft', 'assault', 'fraud', 'robbery', 'vandalism', 'murder']


# ----------------------------------------------------------------
# CALCULATION — number of days since the crime was reported
# ----------------------------------------------------------------
def calculate_case_age_in_days(reported_date):
    # Returns (today - reported_date) as an integer number of days
    return (date.today() - reported_date).days


# ----------------------------------------------------------------
# DISPLAY — print grouped crime summary to console
# ----------------------------------------------------------------
def display_crime_summary(location, grouped):
    print(f"\nCrime Summary for Location: {location}")
    print("=" * 55)
    for crime_type, records in grouped.items():
        print(f"\n[{crime_type}] - {len(records)} case(s)")
        for rec in records:
            age = calculate_case_age_in_days(rec.get_reported_date())
            print(f"  Case No  : {rec.get_case_number()}")
            print(f"  Status   : {rec.get_status()}")
            print(f"  Suspect  : {rec.get_suspect_name()}")
            print(f"  Reported : {rec.get_reported_date().strftime('%d-%m-%Y')}")
            print(f"  Age      : {age} day(s)")
            print()


# ----------------------------------------------------------------
# GROUPING — group a list of CrimeRecords by crime_type into a dict
# ----------------------------------------------------------------
def group_crimes_by_type(crime_list):
    # Keys are title-cased crime types e.g. 'Theft', 'Assault'
    # Raises InvalidCrimeTypeException for any unknown crime type
    grouped = {}
    for rec in crime_list:
        crime_type = rec.get_crime_type()
        if crime_type.lower() not in VALID_CRIME_TYPES:
            raise InvalidCrimeTypeException(
                f"Unknown crime type found in records: {crime_type}")
        key = crime_type.title()
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(rec)
    return grouped


# ----------------------------------------------------------------
# FILE WRITE — export detailed crime report with officer cross-reference
# crime_dao object is passed in so this function stays DB-free in logic
# ----------------------------------------------------------------
def export_crime_report(crime_list, crime_dao, filename):
    try:
        with open(filename, 'w') as f:
            f.write("CRIME REPORT\n")
            f.write("=" * 55 + "\n\n")

            for rec in crime_list:
                age = calculate_case_age_in_days(rec.get_reported_date())
                f.write(f"Case No       : {rec.get_case_number()}\n")
                f.write(f"Crime Type    : {rec.get_crime_type().title()}\n")
                f.write(f"Location      : {rec.get_location()}\n")
                f.write(f"Reported Date : {rec.get_reported_date().strftime('%d-%m-%Y')}\n")
                f.write(f"Case Age      : {age} day(s)\n")
                f.write(f"Status        : {rec.get_status()}\n")
                f.write(f"Suspect       : {rec.get_suspect_name()}\n")

                # Cross-reference officer details from the officer table
                try:
                    officer = crime_dao.retrieve_officer_details(rec.get_officer_id())
                    f.write(f"Officer       : {officer.get_officer_name()} "
                            f"(Badge: {officer.get_badge_number()})\n")
                except OfficerNotFoundException:
                    f.write("Officer       : Details not available\n")

                f.write("-" * 55 + "\n")

    except IOError as e:
        raise IOError(f"Failed to write report: {e}")
