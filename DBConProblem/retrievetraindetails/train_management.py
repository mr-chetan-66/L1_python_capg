### DO NOT ALTER THE GIVEN TEMPLATE.  FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE
import train as tn
import cx_Oracle
 
 
class TrainManagementSystem:
    def __init__(self):
        self.db = ""
        with open('database.properties') as f:
            lines = [line.strip().split("=") for line in f.readlines()
                     if not line.startswith('#') and line.strip()]
            self.db = {key.strip(): value.strip() for key, value in lines}
 
    def retrieve_train_details(self, coach_type, source, destination):
 
        coach_column = coach_type.lower()
        trains = []
 
        try:
            conn = cx_Oracle.connect(
                self.db['DB_USERNAME'],
                self.db['DB_PASSWORD'],
                self.db['DSN']
            )
 
            cursor = conn.cursor()
 
            query = f"""
                SELECT train_number, train_name, source, destination,
                       ac1, ac2, ac3, sleeper, seater
                FROM train
                WHERE LOWER(source) = :source
                  AND LOWER(destination) = :destination
                  AND {coach_column} > 0
                ORDER BY train_number
            """
 
            cursor.execute(
                query,
                {
                    'source': source.lower(),
                    'destination': destination.lower()
                }
            )
 
            rows = cursor.fetchall()
 
            for row in rows:
                t = tn.train(*row)
                trains.append(t)
 
            cursor.close()
            conn.close()
 
        except cx_Oracle.DatabaseError:
            return []
 
        return trains