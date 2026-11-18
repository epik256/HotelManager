import psycopg2
from room import Room
from guest import Guest
import os
from dotenv import load_dotenv

load_dotenv()

#Подключаю датабазу
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),  # Change to your server if needed
    port=os.getenv("DB_PORT")  # Default PostgreSQL port
)

# cur = conn.cursor()
# cur.execute(f'DROP TABLE IF EXISTS rooms CASCADE;')
# cur.execute(f'DROP TABLE IF EXISTS guests CASCADE;')


def create_rooms_db():
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rooms(
                number INTEGER PRIMARY KEY,
                room_type TEXT NOT NULL,
                password INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)

    except psycopg2.Error:
        print("ЧТо то пошло не так...")
        conn.rollback()

    finally:
        conn.commit()
        cur.close()


def add_room_db(room_number, room_type, room_password):
    cur = conn.cursor()


    try:

        cur.execute("SELECT * FROM rooms WHERE number = %s", (room_number,))

        x = cur.fetchone()

        if x is None:
            cur.execute(
                "INSERT INTO rooms (number, room_type, password ) VALUES (%s, %s, %s) ",
                (room_number, room_type, room_password)
            )
            conn.commit()
            return True

        if x[3] == False:


            cur.execute("""
                UPDATE rooms
                SET room_type = %s ,password = %s ,is_active = True
                WHERE number = %s""", (room_type, room_password, room_number))
            conn.commit()
            return True

        else:
            conn.rollback()
            print("Такая комната уже существует!")
            return False



    except psycopg2.errors.UniqueViolation:
        print("КОмната с таким номером уже есть")
        conn.rollback()
        return False
    except psycopg2.errors.Error:
        print("ЧТо то пошло не так...")
        conn.rollback()
        return False
    finally:
        cur.close()

def get_rooms_db():

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM rooms")
        x = cur.fetchall()
        #rooms уже есть в manager!!!
        rooms_db = []

        for room in x:
            room_number = room[0]
            room_type = room[1]
            room_password = room[2]
            room_is_active = room[3]
            room_obj = Room(room_number, room_type, room_password)
            room_obj.is_active = room_is_active
            rooms_db.append(room_obj)


        return rooms_db
    except psycopg2.Error:
        print("ЧТо то пошло не так...")
        conn.rollback()

    finally:
        cur.close()

def update_room_db(room_number, new_password, new_type):

    cur = conn.cursor()

    try:
        if new_type != "Тот же тип":
            update_password = """
                UPDATE rooms
                SET password = %s, room_type = %s
                WHERE number = %s
            """
            cur.execute(update_password, (new_password, new_type, room_number))
            if cur.rowcount > 0:
                conn.commit()
                return True
            else:
                conn.rollback()
                print("КОмнаты с таким номер нет")
                return False
        else:
            update_password = """
                            UPDATE rooms
                            SET password = %s
                            WHERE number = %s
                        """
            cur.execute(update_password, (new_password, room_number))
            if cur.rowcount > 0:
                conn.commit()
                return True
            else:
                conn.rollback()
                print("КОмнаты с таким номер нет")
                return False
    except psycopg2.Error:
        print("ЧТо то пошло не так...")
        conn.rollback()
        return False

    finally:
        cur.close()

def delete_room_db(room_number):

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM guests WHERE room_id = %s AND check_out IS NULL",
            (room_number,))
        x = cur.fetchone()

        if x is None:
            cur.execute(
                """
                UPDATE rooms
                SET is_active = False 
                WHERE number = %s""",
                       (room_number,))
            if cur.rowcount > 0:

                conn.commit()
                return True
            else:
                conn.rollback()
                return False

        else:
            conn.rollback()
            print("В этой комнате еще кто то живет!")
            return False

    except psycopg2.Error:
        conn.rollback()
        return False

    finally:
        cur.close()

def create_guests_db():
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS guests(
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                room_id INTEGER NOT NULL,
                payment_wood INTEGER NOT NULL CHECK (payment_wood >= 0),
                payment_stone INTEGER NOT NULL CHECK (payment_stone >= 0),
                payment_metal INTEGER NOT NULL CHECK (payment_metal >= 0),
                debt_wood INTEGER NOT NULL DEFAULT 0 CHECK (debt_wood >= 0),
                debt_stone INTEGER NOT NULL DEFAULT 0 CHECK (debt_stone >= 0),
                debt_metal INTEGER NOT NULL DEFAULT 0 CHECK (debt_metal >= 0),
                check_in TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                check_out TIMESTAMP WITH TIME ZONE,
                last_debt_update TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_room_id FOREIGN KEY (room_id) REFERENCES rooms(number)
            )
        """)

        # cur.execute("""
        #         CREATE UNIQUE INDEX unique_active_guest_room
        #         ON guests (room_id)
        #         WHERE check_out IS NULL;
        # """)
    except psycopg2.errors.DuplicateTable:
        print("Че то какая то ошибка")
        conn.rollback()
        return False

    except psycopg2.errors.Error:
        print("ЧТо то пошло не так...")
        conn.rollback()

    finally:
        conn.commit()
        cur.close()

def add_guest_db(guest_name, room_number, wood_payment, stone_payment, metal_payment):

    cur = conn.cursor()



    try:

        cur.execute("""
            SELECT is_active
            FROM rooms
            WHERE number = %s
        
        """, (room_number,))

        x = cur.fetchone()

        if x is not None:
            is_active = x[0]

            if is_active == False:
                conn.rollback()
                print("невозможно заселить гостя, такой комнаты нет")
                return None
            else:
                cur.execute(
                    """INSERT INTO guests (name, room_id, payment_wood, payment_stone, payment_metal)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, check_in""",
                    (guest_name, room_number, wood_payment, stone_payment, metal_payment,))
                x = cur.fetchone()

                if x is not None:
                    guest_id = x
                    conn.commit()
                    return guest_id
                else:
                    conn.rollback()
                    return None

        else:
            print("Список пуст, комнаты нет")
            conn.rollback()
            return None





    except psycopg2.errors.ForeignKeyViolation:
        print("Такой комнаты несуществует")
        conn.rollback()
        return None
    except psycopg2.errors.UniqueViolation:
        print("В этой комнает уже кто то проживает")
        conn.rollback()
        return None
    except psycopg2.errors.Error as error:
        print(error)
        conn.rollback()
        return None

    finally:
        cur.close()


def get_guests_db():

    cur = conn.cursor()


    try:
        cur.execute("SELECT * FROM guests")

        guests_db = []

        x = cur.fetchall()


        if x == []:
            conn.rollback()
            print("СПисок гостей пуст")
            return guests_db
        else:
            for guest in x:
                guest_id = guest[0]
                guest_name = guest[1]
                room_id = guest[2]
                wood = guest[3]
                stone = guest[4]
                metal= guest[5]
                debt_w = guest[6]
                debt_s = guest[7]
                debt_m = guest[8]
                check_in = guest[9]
                check_out = guest[10]
                guest_object = Guest(guest_name)
                guest_object.guest_id = guest_id
                guest_object.room_id = room_id
                guest_object.payment["wood"] = int(wood)
                guest_object.payment["stone"] = int(stone)
                guest_object.payment["metal"] = int(metal)
                guest_object.debt["wood"] = int(debt_w)
                guest_object.debt["stone"] = int(debt_s)
                guest_object.debt["metal"] = int(debt_m)
                guest_object.check_in = check_in
                guest_object.check_out = check_out
                guests_db.append(guest_object)

            return guests_db
    finally:
        cur.close()





def update_guest_db(guest_id, new_name, new_wood, new_stone, new_metal, new_room_number):

    cur = conn.cursor()

    try:

        if new_room_number != "Та же комната":
            cur.execute("""
                       SELECT is_active
                       FROM rooms
                       WHERE number = %s
    
                   """, (new_room_number,))

            x = cur.fetchone()

            if x is not None:
                is_active = x[0]

                if is_active == False:
                    conn.rollback()
                    return False
                else:
                    cur.execute("""
                    UPDATE guests
                    SET name = %s,
                    payment_wood = %s,
                    payment_stone = %s,
                    payment_metal = %s,
                    room_id = %s
                    WHERE id = %s AND check_out IS NULL""", (new_name, new_wood, new_stone, new_metal,
                                                             new_room_number, guest_id))

                    if cur.rowcount == 1:
                        conn.commit()
                        return True
                    else:
                        conn.rollback()
                        return False
            else:
                conn.rollback()
                return False
        else:
            cur.execute("""
                UPDATE guests
                SET name = %s,
                payment_wood = %s,
                payment_stone = %s,
                payment_metal = %s
                WHERE id = %s AND check_out IS NULL""", (new_name, new_wood, new_stone,
                                                         new_metal, guest_id))
            if cur.rowcount > 0:
                conn.commit()
                return True
            else:
                conn.rollback()
                return False

    except psycopg2.Error:
        conn.rollback()
        return False
    finally:
        cur.close()


def update_guest_debt_db():
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE guests
            SET
                debt_wood = debt_wood +
                    FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_debt_update)) / 3600)::INTEGER * payment_wood,

                debt_stone = debt_stone +
                    FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_debt_update)) / 3600)::INTEGER * payment_stone,

                debt_metal = debt_metal +
                    FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_debt_update)) / 3600)::INTEGER * payment_metal,

                last_debt_update = last_debt_update +
                    FLOOR(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_debt_update)) / 3600)::INTEGER * INTERVAL '1 hour'

            WHERE check_out IS NULL
            AND CURRENT_TIMESTAMP - last_debt_update >= INTERVAL '1 hour'
        """)

        conn.commit()
        return True

    except psycopg2.Error:
        conn.rollback()
        return False

    finally:
        cur.close()


def pay_debt_db(guest_id, wood, stone, metal):
    cur = conn.cursor()
    try:
        if wood >= 0 and stone >= 0 and metal >= 0:
            cur.execute("""
            UPDATE guests
            SET debt_wood = debt_wood - %s,
            debt_stone = debt_stone - %s,
            debt_metal = debt_metal - %s
            WHERE id = %s
            AND check_out IS NULL
            AND debt_wood >= %s
            AND debt_stone >= %s
            AND debt_metal >= %s
            RETURNING debt_wood, debt_stone, debt_metal""", (wood, stone, metal, guest_id, wood, stone, metal,))

            x = cur.fetchone()




            if x is not None:
                print(x)
                conn.commit()
                return x
            else:
                conn.rollback()
                return None
        else:
            conn.rollback()
            return None

    except psycopg2.Error:
        conn.rollback()
        return None
    finally:
        cur.close()

def check_out_guest_db(guest_id):

    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE guests
            SET check_out = CURRENT_TIMESTAMP
            WHERE id = %s AND check_out is NULL
        """, (guest_id,))

        if cur.rowcount == 0:
            print("Такого гостя нет")
            conn.rollback()
            return False
        elif cur.rowcount == 1:
            conn.commit()
            return True
        else:
            print("Почему то больше одного гостя")
            conn.rollback()
            return False

    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        return False

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False
    except psycopg2.errors.Error:
            print("ЧТо то пошло не так...")
            conn.rollback()
            return False
    finally:
        cur.close()