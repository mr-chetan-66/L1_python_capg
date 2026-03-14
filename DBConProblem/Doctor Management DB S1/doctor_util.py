### doctor_util.py
### Utility / helper functions for Doctor — validation and display

VALID_SPECIALIZATIONS = [
    'cardiology', 'neurology', 'orthopedics', 'dermatology',
    'pediatrics', 'gynecology', 'oncology', 'radiology',
    'psychiatry', 'general surgery'
]


def is_valid_specialization(specialization):
    # Returns True if specialization (case-insensitive) is in VALID_SPECIALIZATIONS
    return specialization.lower() in VALID_SPECIALIZATIONS


def is_valid_experience(experience):
    # Returns True only if experience is a non-negative integer
    return experience >= 0


def display_doctor(doctor):
    print("Doctor ID        :", doctor.get_doctor_id())
    print("Name             :", doctor.get_name())
    print("Specialization   :", doctor.get_specialization())
    print("Hospital         :", doctor.get_hospital())
    print("Experience       :", doctor.get_experience_years(), "years")
    print("Consultation Fee :", doctor.get_consultation_fee())
    print("-" * 40)


def get_result_count(doctor_list):
    return len(doctor_list)


def get_most_affordable(doctor_list):
    # Returns the Doctor object with the lowest consultation fee
    # Returns None if list is empty
    if not doctor_list:
        return None
    return min(doctor_list, key=lambda d: d.get_consultation_fee())


def get_most_experienced(doctor_list):
    # Returns the Doctor object with the highest experience years
    # Returns None if list is empty
    if not doctor_list:
        return None
    return max(doctor_list, key=lambda d: d.get_experience_years())
