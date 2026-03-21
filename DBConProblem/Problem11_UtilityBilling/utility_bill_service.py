### DO NOT ALTER THE GIVEN TEMPLATE. FILL THE CODE ONLY IN THE PROVIDED PLACES ALONE

import oracledb
import utility as ut
import exception as ex
import utility_bill as ub

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class UtilityBillService:

    def __init__(self):
        self.__utility_bill_list = []

    def get_utility_bill_details(self, input_file):
        record=ut.read_file(input_file)
        self.build_utility_bill_list(record)
        self.__utility_bill_list

    def build_utility_bill_list(self, records):
        for line in records:
            part=line.strip().split(",")
            try:
                ut.validate_bill_id(part[0])
                ut.validate_consumer_type(part[3])
                rd=ut.convert_date(part[4])
                bd=ut.convert_date(part[2])
                obj=ub.UtilityBill(part[0],part[1],bd,part[3],rd,float(part[5]),part[6],part[7])

                
            except (ex.InvalidBillIdException,ex.InvalidConsumerTypeException) as e:
                print(e.get_message())

    def calculate_bill_charges(self, units_consumed, consumer_type, connection_type):
       
        # Write your code here
        pass

    def add_utility_bill_details(self, bill_list):
       
        # Write your code here
        pass

    def search_bill(self, bill_id):
        pass

    def update_energy_charges(self, units_threshold):
        pass
