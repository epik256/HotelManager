from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton, QListWidgetItem,
    QDialog,
    QLineEdit,
    QComboBox
)
from PyQt5.QtCore import Qt

from datetime import datetime
from guest import Guest
from manager import Manager
from room import Room

class MainWindow(QMainWindow):

    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.selected_guest = None
        self.check_object = 2
        self.setWindowTitle("Hotel Manager")
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        #Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Главный layout(типо горизонтальная строка)
        master = QHBoxLayout()
        central_widget.setLayout(master)

        #Левая часть
        col1 = QVBoxLayout()

        guest_title = QLabel("ПОСТОЯЛЬЦЫ")

        self.guests_list = QListWidget(central_widget)

        add_button = QPushButton("+ Добавить гостя")
        add_button.clicked.connect(self.add_guest)
        add_room_button = QPushButton("+ Добавить комнату")
        add_room_button.clicked.connect(self.add_room)

        rooms_title = QLabel("КОМНАТЫ")
        self.rooms_list = QListWidget(central_widget)

        col1.addWidget(guest_title)
        col1.addWidget(self.guests_list)
        col1.addWidget(add_button)

        col1.addWidget(rooms_title)
        col1.addWidget(self.rooms_list)
        col1.addWidget(add_room_button)

        #Правая часть
        col2 = QVBoxLayout()

        guest_info = QLabel("ИНФОРМАЦИЯ О ГОСТЕ")
        room_info = QLabel("ИНФОРМАЦИЯ О НОМЕРЕ")

        #Информация гостя
        self.name_label = QLabel()
        self.wood_label = QLabel()
        self.stone_label = QLabel()
        self.metal_label = QLabel()
        self.guest_room_label = QLabel()
        self.check_in_label = QLabel()
        self.time_lived_label = QLabel()

        #Информация комнаты
        self.room_number = QLabel()
        self.room_type = QLabel()
        self.room_password = QLabel()
        self.room_guests = QLabel()

        self.change_button = QPushButton("Изменить")

        col2.addWidget(guest_info)
        col2.addWidget(self.name_label)
        col2.addWidget(self.guest_room_label)
        col2.addWidget(self.check_in_label)
        col2.addWidget(self.time_lived_label)
        col2.addWidget(self.wood_label)
        col2.addWidget(self.stone_label)
        col2.addWidget(self.metal_label)
        col2.addWidget(room_info)
        col2.addWidget(self.room_number)
        col2.addWidget(self.room_type)
        col2.addWidget(self.room_password)
        col2.addWidget(self.room_guests)

        col2.addWidget(self.change_button)

        # Связь
        master.addLayout(col1, 60)
        master.addLayout(col2, 40)

        index = 0
        for guest in self.manager.total_guests:

            item = QListWidgetItem()
            item.setText(f"{index + 1}: {guest.name}")
            item.setData(Qt.UserRole, guest)
            self.guests_list.addItem(item)
            index += 1

        room_index = 0
        for room in self.manager.rooms:

            item = QListWidgetItem()
            item.setText(f"{room_index + 1}: {room.room_type}")
            item.setData(Qt.UserRole, room)
            self.rooms_list.addItem(item)
            room_index += 1

        self.guests_list.itemClicked.connect(self.guest_clicked)
        self.rooms_list.itemClicked.connect(self.room_clicked)
        self.change_button.clicked.connect(self.check)

    def check(self):
        if self.check_object == 0:
            self.change_guest()
        elif self.check_object == 1:
            self.change_room()
        else:
            print("Выберите что изменить")

    def guest_clicked(self, item):
        self.selected_guest = item.data(Qt.UserRole)
        self.check_object = 0
        selected_room = self.selected_guest.room
        self.time_lived = datetime.now() - self.selected_guest.check_in
        total_minutes = int(self.time_lived.total_seconds() // 60)
        hours = total_minutes // 60
        self.selected_guest.calculate_debt(hours)
        minutes = total_minutes % 60
        self.name_label.setText(f"Имя: {self.selected_guest.name}")
        self.guest_room_label.setText(f"Проживает в комнате №{selected_room.number} '{selected_room.room_type}'")
        self.check_in_label.setText(f"Время заселения: {self.selected_guest.check_in.strftime('%H:%M:%S')}")
        #self.wood_label.setText(f"Дерево: {self.selected_guest.payment["wood"]}")
        #self.stone_label.setText(f"Камень: {self.selected_guest.payment["stone"]}")
        #self.metal_label.setText(f"Металл: {self.selected_guest.payment["metal"]}")
        self.wood_label.setText(f"Должен дерева: {self.selected_guest.debt["wood"]}")
        self.stone_label.setText(f"Должен камня: {self.selected_guest.debt["stone"]}")
        self.metal_label.setText(f"Должен металла: {self.selected_guest.debt["metal"]}")

        self.time_lived_label.setText(f"Прожил: {hours}ч {minutes}м")

    def change_guest(self):

            dialog = QDialog()
            dialog.setWindowTitle("Изменить плату")

            layout = QVBoxLayout()
            h1 = QHBoxLayout()
            h2 = QHBoxLayout()
            h3 = QHBoxLayout()
            h4 = QHBoxLayout()

            # лейблы
            wood_label = QLabel("Дерево в час:")
            stone_label = QLabel("Камень в час:")
            metal_label = QLabel("Металл в час:")

            #Вывод инфы
            wood_line = QLineEdit()
            stone_line = QLineEdit()
            metal_line = QLineEdit()

            # Книпка
            self.acchange_button = QPushButton("Подтвердить")

            def change():
                print(self.selected_guest.name)
                wood = wood_line.text()
                stone = stone_line.text()
                metal = metal_line.text()
                if wood.isdigit() and stone.isdigit() and metal.isdigit():
                    self.selected_guest.payment["wood"] = int(wood)
                    self.selected_guest.payment["stone"] = int(stone)
                    self.selected_guest.payment["metal"] = int(metal)
                    self.wood_label.setText(f"Дерево: {self.selected_guest.payment["wood"]}")
                    self.stone_label.setText(f"Камень: {self.selected_guest.payment["stone"]}")
                    self.metal_label.setText(f"Металл: {self.selected_guest.payment["metal"]}")
                    dialog.accept()
                else:
                    print("Вы ввели неккоректные данные")

            self.acchange_button.clicked.connect(change)

            layout.addLayout(h1)
            layout.addLayout(h2)
            layout.addLayout(h3)
            layout.addLayout(h4)

            h2.addWidget(wood_label)
            h2.addWidget(wood_line)
            h3.addWidget(stone_label)
            h3.addWidget(stone_line)
            h4.addWidget(metal_label)
            h4.addWidget(metal_line)
            layout.addWidget(self.acchange_button)
            dialog.setLayout(layout)
            dialog.exec_()

    def add_guest(self):
        #Создаю окно
        dialog = QDialog()
        dialog.setWindowTitle("Добавить гостя")

        #Вертикальная строка виджетов
        layout = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h4 = QHBoxLayout()

        #лейблы
        name_label = QLabel("Имя:")
        wood_label = QLabel("Дерево в час:")
        stone_label = QLabel("Камень в час:")
        metal_label = QLabel("Металл в час:")
        room_label = QLabel("Комната:")

        #Ввод инфы

        name_line = QLineEdit()
        wood_line = QLineEdit()
        stone_line = QLineEdit()
        metal_line = QLineEdit()

        #Книпка
        self.add_button = QPushButton("Добавить")

        #Комбо
        combo = QComboBox()
        combo.addItems(["Нищий", "Стандарт", "Стандарт+"])

        def add():
            name = name_line.text()

            wood = wood_line.text()
            stone = stone_line.text()
            metal = metal_line.text()
            if not name == "" and not name == " " and wood.isdigit() and stone.isdigit() and metal.isdigit():
                room_type = combo.currentText()
                room = Manager.find_free_room(room_type)
                if room is None:
                    print("Такой комнаты нет")
                else:
                    guest = Guest(name)
                    self.manager.total_guests.append(guest)
                    item = QListWidgetItem()
                    item.setData(Qt.UserRole, guest)
                    item.setText(f"{self.guests_list.count() + 1}: {guest.name}")
                    self.guests_list.addItem(item)
                    guest.payment["wood"] = int(wood)
                    guest.payment["stone"] = int(stone)
                    guest.payment["metal"] = int(metal)
                    guest.room = room
                    room.guest = guest
                    self.room_guests.setText(f"Проживает: {guest.name}")
                    dialog.accept()
            else:
                print("Вы ввели неккоректные данные")

        self.add_button.clicked.connect(add)

        # Скрепляю все
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)
        layout.addLayout(h4)

        h1.addWidget(name_label)
        h1.addWidget(name_line)
        h1.addWidget(room_label)
        h1.addWidget(combo)
        h2.addWidget(wood_label)
        h2.addWidget(wood_line)
        h3.addWidget(stone_label)
        h3.addWidget(stone_line)
        h4.addWidget(metal_label)
        h4.addWidget(metal_line)
        layout.addWidget(self.add_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def room_clicked(self, item):
        self.selected_room = item.data(Qt.UserRole)
        self.check_object = 1
        self.room_number.setText(f"Номер: {self.selected_room.number}")
        self.room_type.setText(f"Тип: {self.selected_room.room_type}")
        self.room_password.setText(f"Пароль: {self.selected_room.password}")
        self.room_guests.setText(f"Проживает: {self.selected_room.guest}")

    def change_room(self):
        dialog = QDialog()
        dialog.setWindowTitle("Изменить пароль")

        layout = QHBoxLayout()

        password_label = QLabel("Пароль: ")

        password_line = QLineEdit()

        self.acchange_button = QPushButton("Подтвердить")

        def change():
            if password_line.text().isdigit() and len(password_line.text()) == 4:
                self.selected_room.password = password_line.text()
                self.room_password.setText(f"Пароль: {self.selected_room.password}")
                dialog.accept()
            else:
                print("Пароль должен состоять из 4 цифр")

        self.acchange_button.clicked.connect(change)

        layout.addWidget(password_label)
        layout.addWidget(password_line)
        layout.addWidget(self.acchange_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_room(self):
        dialog = QDialog()
        dialog.setWindowTitle("Добавить комнату")

        #Строки
        layout = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()

        #Лейблы
        number_label = QLabel("Номер:")
        type_label = QLabel("Тип:")
        password_label = QLabel("Пароль:")

        #Ввод
        number_line = QLineEdit()
        combo = QComboBox()
        combo.addItems(["Нищий", "Стандарт", "Стандарт+"])
        password_line = QLineEdit()
        self.add_button = QPushButton("Добавить")

        #Скрепка
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)

        def add():
            number = number_line.text()
            password = password_line.text()
            room_type = combo.currentText()
            if number.isdigit() and password.isdigit() and len(password) == 4:
                if any(str(r.number) == number for r in self.manager.rooms):
                    print("Комната с таким номером уже есть")
                    return
                else:
                    room = Room(number, room_type)
                    room.password = password
                    self.manager.rooms.append(room)
                    item = QListWidgetItem()
                    item.setData(Qt.UserRole, room)
                    self.rooms_list.addItem(item)
                    item.setText(f"{self.rooms_list.count()}: {room.room_type}")

                    dialog.accept()
            else:
                print("низя")

        self.add_button.clicked.connect(add)

        h1.addWidget(number_label)
        h1.addWidget(number_line)
        h2.addWidget(password_label)
        h2.addWidget(password_line)
        h3.addWidget(type_label)
        h3.addWidget(combo)
        layout.addWidget(self.add_button)
        dialog.setLayout(layout)
        dialog.exec_()