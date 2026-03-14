### doctor_dao.py
### Data Access Object — contains all DB query functions for Doctor

import doctor as dc


def retrieve_doctors_by_specialization_and_experience(specialization, min_experience, conn):
    cursor = conn.cursor()

    query = """
        SELECT doctor_id, name, specialization, hospital, experience_years, consultation_fee
        FROM doctor
        WHERE LOWER(specialization) = LOWER(:1)
          AND experience_years >= :2
        ORDER BY consultation_fee ASC
    """

    cursor.execute(query, (specialization, min_experience))
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        return []

    doctor_list = []
    for row in rows:
        doctor_obj = dc.Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
        doctor_list.append(doctor_obj)

    return doctor_list


def retrieve_doctor_by_id(doctor_id, conn):
    cursor = conn.cursor()

    query = """
        SELECT doctor_id, name, specialization, hospital, experience_years, consultation_fee
        FROM doctor
        WHERE doctor_id = :1
    """

    cursor.execute(query, (doctor_id,))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return None

    return dc.Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
