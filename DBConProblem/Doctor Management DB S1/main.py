### main.py
### Entry point — handles user input, calls DAO and utility functions

import db_config as db
import doctor_dao as dao
import doctor_util as util


def main():
    conn = db.get_connection()

    print("=" * 40)
    print("        DOCTOR SEARCH SYSTEM")
    print("=" * 40)

    specialization = input("Enter Specialization        : ")
    min_experience = int(input("Enter Minimum Experience    : "))

    # Validate specialization
    if not util.is_valid_specialization(specialization):
        print("Invalid Specialization")
        return

    # Validate experience
    if not util.is_valid_experience(min_experience):
        print("Invalid Experience")
        return

    result = dao.retrieve_doctors_by_specialization_and_experience(
        specialization, min_experience, conn
    )

    if not result:
        print("No doctors found")
        return

    print("\nTotal Doctors Found :", util.get_result_count(result))
    print("-" * 40)

    # Display all doctors
    for doctor in result:
        util.display_doctor(doctor)

    # Highlight most affordable and most experienced
    affordable  = util.get_most_affordable(result)
    experienced = util.get_most_experienced(result)

    print("=" * 40)
    print("Most Affordable Doctor:")
    print("  Name             :", affordable.get_name())
    print("  Consultation Fee :", affordable.get_consultation_fee())

    print("\nMost Experienced Doctor:")
    print("  Name             :", experienced.get_name())
    print("  Experience       :", experienced.get_experience_years(), "years")
    print("=" * 40)


if __name__ == '__main__':
    main()
