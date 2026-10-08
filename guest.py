from datetime import datetime, timedelta

class Guest:

    def __init__(self, name):
        self.name = name
        self.payment = {}
        self.debt = {"wood": 0,
                     "stone": 0,
                     "metal": 0}
        self.check_in = datetime.now()
        #self.check_in = datetime.now() - timedelta(minutes=125)
        self.check_out = None
        self.room = None

    def __repr__(self):
        return f"{self.name}"

    def calculate_debt(self, hours):
        self.debt["wood"] = hours * self.payment["wood"]
        self.debt["stone"] = hours * self.payment["stone"]
        self.debt["metal"] = hours * self.payment["metal"]


