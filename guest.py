from datetime import datetime, timedelta, timezone

class Guest:

    def __init__(self, name):
        self.name = name
        self.guest_id = None
        self.payment = {}
        self.debt = {"wood": 0,
                     "stone": 0,
                     "metal": 0}
        self.check_in = datetime.now(timezone.utc)
        #self.check_in = datetime.now(timezone.utc) - timedelta(minutes=125)
        self.check_out = None
        self.room = None
        self.room_id = None

    def __repr__(self):
        return f"({self.name}({self.guest_id}) живет в {self.room_id}; заселился: {self.check_in.strftime('%H:%M')} {self.check_out}, Долг:{self.debt})"


