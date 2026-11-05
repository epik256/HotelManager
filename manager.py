
from DATABASE.database import (get_rooms_db,
                               get_guests_db,
                               add_guest_db,
                               add_room_db,
                               delete_room_db,
                               check_out_guest_db,
                               update_room_db,
                               update_guest_db, update_guest_debt_db, pay_debt_db
                               )
from guest import Guest

from room import Room
from datetime import datetime, timezone

class Manager:
    def __init__(self):
        self.rooms = []
        self.total_guests = []
        self.deleted_guests = []


    def find_free_room(self, room_type):

        succ_find = None
        for room in self.rooms:
            if succ_find == None:
                if room.room_type == room_type and room.guest is None and room.is_active == True:
                    succ_find = room
                else:
                    succ_find = None
        return succ_find




    def restore_rooms(self):

        if self.rooms:
            return False

        rooms_db = get_rooms_db()


        for room in rooms_db:
            if room in self.rooms:
                return False
            else:
                self.rooms.append(room)
        return self.rooms



    def add_room(self, number, room_type, room_password):

        room = next(
            (r for r in self.rooms if r.number == number and not r.is_active),
            None
        )

        if any(r.number == number and r.is_active == True for r in self.rooms):
            print("Дубликат комнаты в self.rooms")
            return None
        elif room is not None:
            success = add_room_db(number, room_type, room_password)
            if success:
                room.is_active = True
                room.password = room_password
                room.room_type = room_type
                return room
            else:
                return None

        else:
            success = add_room_db(number, room_type, room_password)
            if success:
                room_obj = Room(number, room_type, room_password)
                self.rooms.append(room_obj)
                return room_obj
            else:
                return None

    def delete_room(self, room_number):

        room = next(
            (r for r in self.rooms if r.number == room_number and r.is_active),
            None
        )

        if room is not None:

            delete = delete_room_db(room_number)
            if delete == True:
                room.is_active = False
                return True
            else:
                return False
        else:
            return None

    def change_room(self, room_number, password, room_type):

        room = next(
            (r for r in self.rooms if r.number == room_number and r.is_active),
            None
        )

        if room:

            update = update_room_db(room_number, password, room_type)
            if update == True:
                if room_type != "Тот же тип":
                    room.password = password
                    room.room_type = room_type
                    return True
                else:
                    room.password = password
                    return True
            else:
                return False
        else:
            return False


    def restore_guests(self):

        if self.total_guests or self.deleted_guests:
            return False


        if self.rooms == []:
            return False
        else:
            guests_db = get_guests_db()

            rooms_by_number = {
                room.number: room
                for room in self.rooms
            }

            for guest in guests_db:

                found_room = rooms_by_number.get(guest.room_id)

                if found_room is None:
                    return False

                if guest.check_out is None:
                    if not found_room.is_active:
                        return False

                    if found_room.guest is not None:
                        return False

            # Второй проход — восстановление связей
            for guest in guests_db:


                found_room = rooms_by_number[guest.room_id]
                guest.room = found_room

                if guest.check_out is None:
                    found_room.guest = guest
                    self.total_guests.append(guest)
                else:
                    self.deleted_guests.append(guest)

            return True


    def add_guest(self, name, payment, room_type):

        find_room = self.find_free_room(room_type)

        if find_room is None:
            print("find_fre_room1")
            return None

        guest_id = add_guest_db(name, find_room.number, int(payment[0]), int(payment[1]), int(payment[2]))
        if guest_id is not None:
            guest = Guest(name)
            guest.guest_id = guest_id[0]
            guest.room_id = find_room.number
            guest.payment["wood"] = int(payment[0])
            guest.payment["stone"] = int(payment[1])
            guest.payment["metal"] = int(payment[2])
            find_room.guest = guest
            guest.room = find_room
            self.total_guests.append(guest)
            guest.check_in = guest_id[1]
            return guest
        else:
            print("guest_id = None")
            return None


    def change_guest(self, guest_id, new_name, new_wood, new_stone, new_metal, new_room):

        guest = next(
            (g for g in self.total_guests if g.guest_id == guest_id and g.check_out is None),
            None
        )


        if new_room != "Та же комната":
            find_room = self.find_free_room(new_room)

            if find_room is None:
                print(3)
                return False


            if guest:
                update = update_guest_db(guest_id, new_name, int(new_wood), int(new_stone), int(new_metal), find_room.number)
                if update == True:
                    guest.room.guest = None
                    guest.name = new_name
                    guest.room_id = find_room.number
                    guest.payment["wood"] = int(new_wood)
                    guest.payment["stone"] = int(new_stone)
                    guest.payment["metal"] = int(new_metal)
                    find_room.guest = guest
                    guest.room = find_room
                    print(self.rooms)
                    print(self.total_guests)
                    return guest
                else:
                    return False
            else:
                return False
        else:
            if guest:
                update = update_guest_db(guest_id, new_name, new_wood, new_stone, new_metal, new_room)
                if update == True:
                    guest.name = new_name
                    guest.payment["wood"] = int(new_wood)
                    guest.payment["stone"] = int(new_stone)
                    guest.payment["metal"] = int(new_metal)
                    print(self.rooms)
                    print(self.total_guests)
                    return guest
                else:
                    return False
            else:
                return False

    def pay_debt(self, guest_id, wood, stone, metal):

        guest = next(
            (g for g in self.total_guests if g.guest_id == guest_id and g.check_out is None),
            None
        )


        if guest:
            update_db = update_guest_debt_db()
            if update_db:
                pay_db = pay_debt_db(guest_id, int(wood), int(stone),  int(metal))
                if pay_db:
                    guest.debt["wood"] = pay_db[0]
                    guest.debt["stone"] = pay_db[1]
                    guest.debt["metal"] = pay_db[2]
                    return True
                else:
                    return False
            return False
        else:
            return False


    def delete_guest(self, guest_id):

        guest = next(
            (g for g in self.total_guests if g.guest_id == guest_id and g.check_out is None),
            None
        )
        if guest is not None:
            check_out = check_out_guest_db(guest_id)
            if check_out == True:

                room = guest.room
                room.guest = None
                guest.check_out = datetime.now(timezone.utc)
                self.deleted_guests.append(guest)
                return True
            else:
                print("Датабаза")
                return False
        else:
            print("Список manager")
            return False


