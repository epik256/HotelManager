


class Room:
    def __init__(self, number, room_type, password):
        self.number = number
        self.room_type = room_type
        self.password = password
        self.is_active = True
        self.guest = None

    def __repr__(self):
        return f"Комната№{self.number}({self.room_type}) пароль{self.password}; активна:{self.is_active}; проживает:{self.guest}"


