

class Manager:

    rooms = []

    def __init__(self):
        self.total_guests = []
        self.deleted_guests = []

    @classmethod
    def find_free_room(cls, room_type):
        for room in cls.rooms:
            if room.room_type == room_type and room.guest is None:
                return room
        return None