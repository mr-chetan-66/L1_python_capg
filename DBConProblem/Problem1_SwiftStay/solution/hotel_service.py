import utility as ut
import hotel_booking as hb
from datetime import timedelta
import oracledb
import hotel_exception as he

db = {}
with open("database.properties") as f:
    lines = [line.strip().split("=") for line in f if not line.startswith("#") and line.strip()]
    db = {k.strip(): v.strip() for k, v in lines}
conn = oracledb.connect(user=db["DB_USERNAME"], password=db["DB_PASSWORD"], dsn=db["DSN"])


class HotelService:

    def __init__(self):
        self.__tax_dict = {}

    def read_data(self, records):
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE HotelBooking")
        for line in records:
            part = line.strip().split(",")
            try:
                ut.validate_room_number(part[1])
                ut.validate_booking_id(part[0])
                d = ut.convert_date(part[5])
                obj = hb.HotelBooking(part[0], part[1], part[2],
                                      float(part[3]), int(part[4]), d, part[6])
                base = obj.calculate_base_amount()
                tax, total = self.calculate_tax(part[6], base)
                obj.set_tax_amount(tax)
                obj.set_total_amount(total)
                self.add_booking_details(obj)
                self.__tax_dict[obj.get_booking_id()] = tax
            except he.InvalidRoomNumberException as e:
                print(e.get_message())
            except he.InvalidBookingIdException as e:
                print(e.get_message())
        return None

    def calculate_tax(self, room_type, base_amount):
        if room_type == "Suite":
            rate = 0.18
        elif room_type == "Deluxe":
            rate = 0.12
        else:  # Standard
            rate = 0.08
        tax = base_amount * rate
        total = base_amount + tax
        return tax, total

    def add_booking_details(self, obj):
        with conn.cursor() as cur:
            q = 'insert into HotelBooking values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)'
            l = [obj.get_booking_id(), obj.get_room_number(), obj.get_guest_name(),
                 obj.get_room_rate(), obj.get_no_of_nights(), obj.get_check_in_date(),
                 obj.get_room_type(), obj.get_base_amount(), obj.get_tax_amount(),
                 obj.get_total_amount()]
            cur.execute(q, l)
            conn.commit()
        return None

    def find_top3_rooms(self):
        with conn.cursor() as cur:
            cur.execute("select * from HotelBooking")
            rows = cur.fetchall()
            room_dict = {}
            for row in rows:
                room_num = row[1]
                if room_num in room_dict:
                    room_dict[room_num] += 1
                else:
                    room_dict[room_num] = 1

            sorted_dict = dict(sorted(room_dict.items(), key=lambda x: x[1], reverse=True))

            res_dict = {}
            i = 0
            prev = 0
            for x, y in sorted_dict.items():
                if y != prev:
                    prev = y
                    i += 1
                if i > 3:
                    break
                res_dict[x] = y
            return res_dict

    def search_booking(self, booking_id):
        with conn.cursor() as cur:
            q = "select * from HotelBooking where booking_id=:1"
            cur.execute(q, (booking_id,))
            row = cur.fetchone()
            if row is None:
                return None
            obj = hb.HotelBooking(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            obj.set_base_amount(row[7])
            obj.set_tax_amount(row[8])
            obj.set_total_amount(row[9])
            return obj

    def find_checkout_dates(self, start_date, end_date):
        with conn.cursor() as cur:
            q = """select booking_id, check_in_date, no_of_nights from HotelBooking
                   where no_of_nights > 5
                   and check_in_date between :1 and :2"""
            cur.execute(q, (start_date, end_date))
            rows = cur.fetchall()
            return {bid: (d + timedelta(days=nd)) for bid, d, nd in rows}

    def update_tax_rates(self, room_type):
        with conn.cursor() as cur:
            q1 = """update HotelBooking
                    set tax_amount = tax_amount * 1.1,
                        total_amount = base_amount + (tax_amount * 1.1)
                    where room_type = :1"""
            cur.execute(q1, (room_type,))
            conn.commit()

            q2 = "select * from HotelBooking where room_type = :1"
            cur.execute(q2, (room_type,))
            rows = cur.fetchall()
            if not rows:
                return None
            result = []
            for row in rows:
                obj = hb.HotelBooking(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                obj.set_base_amount(row[7])
                obj.set_tax_amount(row[8])
                obj.set_total_amount(row[9])
                result.append(obj)
            return result
