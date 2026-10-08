import sys

from PyQt5.QtWidgets import QApplication


from guest import Guest
from manager import Manager
from room import Room
from ui.main_window import MainWindow


app = QApplication(sys.argv)

manager = Manager()





window = MainWindow(manager)


window.show()

sys.exit(app.exec_())