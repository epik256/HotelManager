import sys
from PyQt5.QtWidgets import QApplication


from manager import Manager
from ui.main_window import MainWindow
from DATABASE.database import (create_rooms_db,
                               create_guests_db,
                               add_room_db,
                               get_rooms_db,
                               update_room_db,
                               delete_room_db,
                               add_guest_db,
                               get_guests_db,
                               check_out_guest_db,
                               update_guest_debt_db,
                               pay_debt_db)

app = QApplication(sys.argv)
manager = Manager()

create_rooms_db()
create_guests_db()

#add_guest_db("Charlie", 1, 110, 500, 200)
#check_out_guest_db(6)
#add_guest_db("Lol", 1, 210, 400, 300)
#add_guest_db("Kira", 2, 610, 100, 250)
#



manager.restore_rooms()
update_guest_debt_db()
manager.restore_guests()

window = MainWindow(manager)
window.show()



# room1 = Room(1, "Стандарт")
# room1.password = 3331
# room2 = Room(2, "Стандарт")
# room2.password = 2220
#room3 = Room(3, "Нищая")
#room3.password = 2231
#room4 = Room(4, "Богатая")
#room4.password = 4532
# room5 = Room(5, "Нищая")
# room5.password = 6666


#add_room_db(room4)
print(manager.rooms)
print(manager.total_guests)
# print(manager.deleted_guests)





sys.exit(app.exec_())