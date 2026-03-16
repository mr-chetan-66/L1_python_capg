import oracledb

conn  = oracledb.connect(
            user="system",
            password="12345",
            dsn = oracledb.makedsn("10.110.182.9", 1521, sid="XE")
        )
cursor = conn.cursor()
query="""CREATE TABLE reimbursement (
    request_id                VARCHAR2(100),
    employee_code             VARCHAR2(100),
    date_of_request           DATE,
    grade                     VARCHAR2(50),
    date_of_travel            DATE,
    no_of_days_of_stay        NUMBER,
    local_travel_in_kms       NUMBER(10,2),
    manager_approval          VARCHAR2(50),
    accomodation_cost         NUMBER(12,2),
    dining_cost               NUMBER(12,2),
    allowances                NUMBER(12,2),
    local_travel_cost         NUMBER(12,2),
    total_reimbursement_cost  NUMBER(12,2)
)"""
cursor.execute(query)
conn.commit()
print("done")