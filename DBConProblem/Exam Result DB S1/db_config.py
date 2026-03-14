### db_config.py
### Reads DB credentials from database.properties and returns a connection

import cx_Oracle


def get_connection():
    with open('database.properties') as f:
        lines = [line.strip().split("=") for line in f.readlines()
                 if not line.startswith('#') and line.strip()]
        db = {key.strip(): value.strip() for key, value in lines}

    conn = cx_Oracle.connect(db['DB_USERNAME'], db['DB_PASSWORD'], db['DSN'])
    return conn
