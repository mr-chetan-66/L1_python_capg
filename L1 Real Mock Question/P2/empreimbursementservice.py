# empreimbursement_service.py
from typing import List, Optional, Tuple
import os
import configparser
import cx_Oracle  # Ensure this is installed in your runtime


from datetime import date as date_cls
from empreimbursement import EmpReimbursement
from utility import (read_file, validate_request_id, convert_date,
                     InvalidRequestIdException)

class EmpReimbursementService:
    def __init__(self):
        self.emp_reimbursement_list: List[EmpReimbursement] = []

    # ---------------- Public API ----------------

    def get_emp_reimbursement_details(self, input_txt_file: str) -> List[EmpReimbursement]:
        recs = read_file(input_txt_file)
        self.build_emp_reimbursement_list(recs)
        return self.emp_reimbursement_list

    def calculate_reimbursement_costs(self, no_of_days: int, local_kms_travel: float, grade: str) -> List[float]:

        level = self._extract_level(grade)
        if level in (1, 2):
            acc_per_day, dine_per_day, local_per_km, allow_per_day = 10000, 1000, 22, 1500
        elif level in (3, 4):
            acc_per_day, dine_per_day, local_per_km, allow_per_day = 4000, 700, 16, 1000
        elif level in (5, 6):
            acc_per_day, dine_per_day, local_per_km, allow_per_day = 2500, 450, 12, 750
        else:
            raise ValueError(f"Unsupported grade/level: {grade}")

        accomodation_cost = acc_per_day * no_of_days
        dining_cost = dine_per_day * no_of_days
        local_travel_cost = local_per_km * float(local_kms_travel)
        allowances = allow_per_day * no_of_days
        total_reimbursement_cost = accomodation_cost + dining_cost + local_travel_cost + allowances

        return [
            float(accomodation_cost),
            float(dining_cost),
            float(local_travel_cost),
            float(allowances),
            float(total_reimbursement_cost),
        ]

    def build_emp_reimbursement_list(self, records: List[str]) -> None:
        for line in records:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 8:
                continue

            (request_id, employee_code, date_of_request_s, grade,
             date_of_travel_s, no_of_days_s, local_travel_in_kms_s,
             manager_approval, *_) = parts

            try:
                # Validate request id
                validate_request_id(request_id)

                # Convert dates & numeric
                date_of_request = convert_date(date_of_request_s)
                date_of_travel = convert_date(date_of_travel_s)
                no_of_days_of_stay = int(float(no_of_days_s))
                local_travel_in_kms = float(local_travel_in_kms_s)

                # Create object
                emp = EmpReimbursement(
                    request_id=request_id,
                    employee_code=employee_code,
                    date_of_request=date_of_request,
                    grade=grade,
                    date_of_travel=date_of_travel,
                    no_of_days_of_stay=no_of_days_of_stay,
                    local_travel_in_kms=local_travel_in_kms,
                    manager_approval=manager_approval
                )

                # Calculate costs
                acc, dine, local, allow, total = self.calculate_reimbursement_costs(
                    no_of_days=no_of_days_of_stay,
                    local_kms_travel=local_travel_in_kms,
                    grade=grade
                )

                # Set costs
                emp.set_accomodation_cost(acc)
                emp.set_dining_cost(dine)
                emp.set_local_travel_cost(local)
                emp.set_allowances(allow)
                emp.set_total_reimbursement_cost(total)

                # Append
                self.emp_reimbursement_list.append(emp)

            except InvalidRequestIdException:
                # Skip invalid request_id rows in file
                continue
            except Exception:
                # Skip any malformed rows
                continue

    def add_reimbursement_details(self, emp_list: List[EmpReimbursement]) -> None:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError("Oracle client not available (cx_Oracle missing).")

        insert_sql = """
            INSERT INTO reimbursement (
                request_id, employee_code, date_of_request, grade, date_of_travel,
                no_of_days_of_stay, local_travel_in_kms, manager_approval,
                accomodation_cost, dining_cost, allowances, local_travel_cost, total_reimbursement_cost
            ) VALUES (
                :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13
            )
        """
        try:
            with conn:
                with conn.cursor() as cur:
                    for e in emp_list:
                        cur.execute(insert_sql, [
                            e.get_request_id(),
                            e.get_employee_code(),
                            e.get_date_of_request(),
                            e.get_grade(),
                            e.get_date_of_travel(),
                            int(e.get_no_of_days_of_stay()),
                            float(e.get_local_travel_in_kms()),
                            e.get_manager_approval(),
                            float(e.get_accomodation_cost()),
                            float(e.get_dining_cost()),
                            float(e.get_allowances()),
                            float(e.get_local_travel_cost()),
                            float(e.get_total_reimbursement_cost()),
                        ])
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def search_reimbursement_request(self, request_id: str) -> Optional[EmpReimbursement]:
        """
        Find row by request_id and return EmpReimbursement or None.
        """
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError("Oracle client not available (cx_Oracle missing).")

        select_sql = """
            SELECT request_id, employee_code, date_of_request, grade, date_of_travel,
                   no_of_days_of_stay, local_travel_in_kms, manager_approval,
                   accomodation_cost, dining_cost, allowances, local_travel_cost, total_reimbursement_cost
            FROM reimbursement
            WHERE request_id = :rid
        """
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(select_sql, rid=request_id)
                    row = cur.fetchone()
                    if not row:
                        return None

                    # Build object
                    (rid, emp_code, dor, grade, dot,
                     days, kms, appr, acc, dine, allow, local, total) = row

                    emp = EmpReimbursement(
                        request_id=rid,
                        employee_code=emp_code,
                        date_of_request=dor,
                        grade=grade,
                        date_of_travel=dot,
                        no_of_days_of_stay=int(days),
                        local_travel_in_kms=float(kms),
                        manager_approval=appr
                    )
                    emp.set_accomodation_cost(float(acc))
                    emp.set_dining_cost(float(dine))
                    emp.set_allowances(float(allow))
                    emp.set_local_travel_cost(float(local))
                    emp.set_total_reimbursement_cost(float(total))
                    return emp
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def update_costs(self, no_days: int) -> List[EmpReimbursement]:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError("Oracle client not available (cx_Oracle missing).")

        # Update and return updated rows
        select_sql = """
            SELECT request_id, employee_code, date_of_request, grade, date_of_travel,
                   no_of_days_of_stay, local_travel_in_kms, manager_approval,
                   accomodation_cost, dining_cost, allowances, local_travel_cost, total_reimbursement_cost
            FROM reimbursement
            WHERE no_of_days_of_stay > :nd
        """
        update_sql = """
            UPDATE reimbursement
            SET allowances = :new_allow,
                local_travel_cost = :new_local,
                total_reimbursement_cost = :new_total
            WHERE request_id = :rid
        """

        updated: List[EmpReimbursement] = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(select_sql, nd=int(no_days))
                    rows = cur.fetchall()
                    for row in rows:
                        (rid, emp_code, dor, grade, dot,
                         days, kms, appr, acc, dine, allow, local, total) = row

                        new_allow = float(allow) * 1.10
                        new_local = float(local) * 1.10
                        # Recompute total by delta increase
                        delta = (new_allow - float(allow)) + (new_local - float(local))
                        new_total = float(total) + delta

                        cur.execute(update_sql, new_allow=new_allow, new_local=new_local,
                                    new_total=new_total, rid=rid)

                        emp = EmpReimbursement(
                            request_id=rid,
                            employee_code=emp_code,
                            date_of_request=dor,
                            grade=grade,
                            date_of_travel=dot,
                            no_of_days_of_stay=int(days),
                            local_travel_in_kms=float(kms),
                            manager_approval=appr
                        )
                        emp.set_accomodation_cost(float(acc))
                        emp.set_dining_cost(float(dine))
                        emp.set_allowances(float(new_allow))
                        emp.set_local_travel_cost(float(new_local))
                        emp.set_total_reimbursement_cost(float(new_total))
                        updated.append(emp)
        finally:
            try:
                conn.close()
            except Exception:
                pass

        return updated

    # ---------------- Internals ----------------

    def _extract_level(self, grade: str) -> int:
        import re
        m = re.search(r"(\d+)", grade or "")
        if not m:
            raise ValueError(f"Cannot parse grade level from: {grade}")
        return int(m.group(1).lstrip("0") or "0")

    def _get_connection(self):
        if cx_Oracle is None:
            return None
        props = self._read_db_props()
        user = props.get("db.user")
        pwd = props.get("db.password")
        host = props.get("db.host")
        port = props.get("db.port", "1521")
        svc = props.get("db.service_name")
        dsn = cx_Oracle.makedsn(host, int(port), service_name=svc)
        return cx_Oracle.connect(user=user, password=pwd, dsn=dsn)

    @staticmethod
    def _read_db_props() -> dict:

        props_path = os.path.join(os.getcwd(), "database.properties")
        if not os.path.exists(props_path):
            raise FileNotFoundError("database.properties not found in current directory.")
        # Parse simple key=value properties
        config = configparser.ConfigParser()
        # Trick: configparser needs a section; fake one for .properties
        with open(props_path, "r", encoding="utf-8") as f:
            content = f.read()
        content_wrapped = "[DEFAULT]\n" + content
        config.read_string(content_wrapped)
        return dict(config["DEFAULT"])