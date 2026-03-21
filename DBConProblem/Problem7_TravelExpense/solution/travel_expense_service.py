import oracledb
import utility as ut
import exception as ex
import travel_expense as te

db = ""
with open('database.properties') as f:
    lines = [line.strip().split("=") for line in f.readlines() if not line.startswith('#') and line.strip()]
    db = {key.strip(): value.strip() for key, value in lines}

conn = oracledb.connect(user=db['DB_USERNAME'], password=db['DB_PASSWORD'], dsn=db['DSN'])


class TravelExpenseService:

    def __init__(self):
        self.__travel_expense_list = []

    def get_travel_expense_details(self, input_file):
        records = ut.read_file(input_file)
        self.build_travel_expense_list(records)
        return self.__travel_expense_list

    def build_travel_expense_list(self, records):
        for line in records:
            try:
                row = line.strip().split(",")
                ut.validate_expense_id(row[0])
                ut.validate_city_tier(row[3])

                dot = ut.convert_date(row[2])
                dor = ut.convert_date(row[4])

                obj = te.TravelExpense(row[0], row[1], dot, row[3], dor,
                                       int(row[5]), row[6], row[7])

                costs = self.calculate_travel_costs(int(row[5]), row[3], row[6])
                obj.set_flight_or_transport_cost(costs[0])
                obj.set_hotel_cost(costs[1])
                obj.set_meal_cost(costs[2])
                obj.set_incidental_allowance(costs[3])
                obj.set_total_expense(costs[4])

                self.__travel_expense_list.append(obj)

            except ex.InvalidExpenseIdException as e:
                print(e.get_message())
            except ex.InvalidCityTierException as e:
                print(e.get_message())

        return None

    def calculate_travel_costs(self, no_of_days, city_tier, travel_mode):
        # Step 1: City-tier daily rates
        tier_rates = {
            'Tier1': (5000.0, 1200.0, 500.0),
            'Tier2': (2500.0, 700.0,  300.0),
            'Tier3': (1200.0, 400.0,  150.0),
        }
        hotel_rate, meal_rate, incid_rate = tier_rates[city_tier]

        hotel_cost           = hotel_rate * no_of_days
        meal_cost            = meal_rate  * no_of_days
        incidental_allowance = incid_rate * no_of_days

        # Step 2: Transport cost with city_tier_factor
        tier_factor = {'Tier1': 2.0, 'Tier2': 1.5, 'Tier3': 1.0}
        factor = tier_factor[city_tier]

        mode_base = {'Flight': 8000.0, 'Train': 1500.0, 'Bus': 800.0}
        if travel_mode == 'Own Vehicle':
            flight_or_transport_cost = 500.0
        else:
            flight_or_transport_cost = mode_base[travel_mode] * factor

        # Step 3: Total
        total_expense = (flight_or_transport_cost + hotel_cost
                         + meal_cost + incidental_allowance)

        return [flight_or_transport_cost, hotel_cost, meal_cost,
                incidental_allowance, total_expense]

    def add_travel_expense_details(self, expense_list):
        with conn.cursor() as cur:
            for obj in expense_list:
                q = """insert into travel_expense values
                       (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"""
                l = [obj.get_expense_id(), obj.get_employee_id(),
                     obj.get_date_of_travel(), obj.get_city_tier(),
                     obj.get_date_of_return(), obj.get_no_of_days(),
                     obj.get_travel_mode(), obj.get_approval_status(),
                     obj.get_flight_or_transport_cost(), obj.get_hotel_cost(),
                     obj.get_meal_cost(), obj.get_incidental_allowance(),
                     obj.get_total_expense()]
                cur.execute(q, l)
                conn.commit()
        return None

    def search_expense(self, expense_id):
        with conn.cursor() as cur:
            q = """select * from travel_expense where expense_id=:1"""
            cur.execute(q, (expense_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = te.TravelExpense(row[0], row[1], row[2], row[3], row[4],
                                   row[5], row[6], row[7])
            obj.set_flight_or_transport_cost(row[8])
            obj.set_hotel_cost(row[9])
            obj.set_meal_cost(row[10])
            obj.set_incidental_allowance(row[11])
            obj.set_total_expense(row[12])
            return obj

    def update_meal_cost(self, no_of_days_threshold):
        with conn.cursor() as cur:
            q1 = """update travel_expense
                    set meal_cost            = meal_cost * 1.12,
                        incidental_allowance = incidental_allowance * 1.12,
                        total_expense        = flight_or_transport_cost + hotel_cost
                                               + meal_cost * 1.12
                                               + incidental_allowance * 1.12
                    where no_of_days > :1"""
            cur.execute(q1, (no_of_days_threshold,))
            conn.commit()

            q2 = """select * from travel_expense where no_of_days > :1"""
            cur.execute(q2, (no_of_days_threshold,))
            rows = cur.fetchall()

            if not rows:
                return None

            ans = []
            for obj in rows:
                sobj = te.TravelExpense(obj[0], obj[1], obj[2], obj[3], obj[4],
                                        obj[5], obj[6], obj[7])
                sobj.set_flight_or_transport_cost(obj[8])
                sobj.set_hotel_cost(obj[9])
                sobj.set_meal_cost(obj[10])
                sobj.set_incidental_allowance(obj[11])
                sobj.set_total_expense(obj[12])
                ans.append(sobj)
            return ans
