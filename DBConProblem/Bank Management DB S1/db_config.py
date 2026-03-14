### db_config.py
### Handles reading database.properties and returning a live cx_Oracle connection

import cx_Oracle

def get_connection():
    db = {}
    with open('database.properties') as f:
        lines = [line.strip().split("=") for line in f.readlines()
                 if not line.startswith('#') and line.strip()]
        db = {key.strip(): value.strip() for key, value in lines}

    conn = cx_Oracle.connect(db['DB_USERNAME'], db['DB_PASSWORD'], db['DSN'])
    return conn
