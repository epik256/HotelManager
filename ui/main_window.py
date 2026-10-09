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
    QComboBox,
    QStackedWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt

from datetime import datetime

from guest import Guest
from manager import Manager
from room import Room
from ui.style_sheets import DIALOG_STYLE, MAIN_STYLE


class MainWindow(QMainWindow):

    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.selected_guest = None
        self.check_object = 2
        self.setWindowTitle("Hotel Manager")
        self.resize(1000, 700)
        self.init_ui()
        self.setStyleSheet(MAIN_STYLE)

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

        self.info_stack = QStackedWidget()

        info_label = QLabel("ИНФОРМАЦИЯ")





        #Информация гостя
        guest_page = QWidget()
        guest_layout = QVBoxLayout()
        self.name_label = QLabel()
        self.wood_label = QLabel()
        self.stone_label = QLabel()
        self.metal_label = QLabel()
        self.guest_room_label = QLabel()
        self.check_in_label = QLabel()
        self.time_lived_label = QLabel()

        #Информация комнаты
        room_page = QWidget()
        room_layout = QVBoxLayout()
        self.room_number = QLabel()
        self.room_type = QLabel()
        self.room_password = QLabel()
        self.room_guests = QLabel()

        self.change_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")


        #Добавляю все

        guest_layout.addWidget(self.name_label)
        guest_layout.addWidget(self.guest_room_label)
        guest_layout.addWidget(self.check_in_label)
        guest_layout.addWidget(self.time_lived_label)
        guest_layout.addWidget(self.wood_label)
        guest_layout.addWidget(self.stone_label)
        guest_layout.addWidget(self.metal_label)

        room_layout.addWidget(self.room_number)
        room_layout.addWidget(self.room_type)
        room_layout.addWidget(self.room_password)
        room_layout.addWidget(self.room_guests)

        col2.addWidget(info_label)
        col2.addWidget(self.info_stack, 1)



        col2.addWidget(self.change_button)
        col2.addWidget(self.delete_button)
        # Связь
        guest_page.setLayout(guest_layout)
        room_page.setLayout(room_layout)

        self.info_stack.addWidget(guest_page)
        self.info_stack.addWidget(room_page)


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
        self.change_button.clicked.connect(self.change_check)
        self.delete_button.clicked.connect(self.delete_check)

    def delete_check(self):

        if self.check_object == 0:
            self.delete_guest()
        elif self.check_object == 1:
            self.delete_room()
        else:
            print("Выберите что удалить")

    def change_check(self):
        if self.check_object == 0:
            self.change_guest()
        elif self.check_object == 1:
            self.change_room()
        else:
            print("Выберите что изменить")

    def guest_clicked(self, item):
        self.info_stack.setCurrentIndex(0)
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
        self.check_in_label.setText(f"Время заселения: {self.selected_guest.check_in.strftime('%H:%M')}")
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
            dialog.setStyleSheet(DIALOG_STYLE)

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
                    QMessageBox.information(
                        dialog,
                        "Успешно",
                        "Гость был успешно изменен!"
                    )
                    dialog.accept()
                else:
                    QMessageBox.warning(
                        dialog,
                        "Ошибка",
                        "Вы ввели некорректные данные"
                    )

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
        dialog.setStyleSheet(DIALOG_STYLE)

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
                    QMessageBox.warning(
                        dialog,
                        "Ошибка",
                        "Комнаты с таким типом нет. Измените тип комнаты либо добавьте новую"
                    )
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
                    QMessageBox.information(
                        dialog,
                        "Успешно",
                        "Гость был успешно добавлен!"
                    )
                    dialog.accept()
            else:
                QMessageBox.warning(
                    dialog,
                    "Ошибка ввода",
                    "Проверьте правильность введённых данных!"
                )

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

    def delete_guest(self):
        dialog = QDialog()
        dialog.setWindowTitle("Удалить")
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        yes_button = QPushButton("Да")
        no_button = QPushButton("Нет")

        sure_label = QLabel(f"Вы уверены что хотите удалить {self.selected_guest.name}?")

        def yes():
            item = self.guests_list.currentItem()
            self.manager.total_guests.remove(self.selected_guest)
            self.guests_list.takeItem(self.guests_list.row(item))
            self.selected_guest.room.guest = None
            self.name_label.setText("")
            self.guest_room_label.setText("")
            self.check_in_label.setText("")
            self.wood_label.setText("")
            self.stone_label.setText("")
            self.metal_label.setText("")
            self.time_lived_label.setText("")
            QMessageBox.information(
                dialog,
                "Успешно",
                "Гость был успешно удален!"
            )
            dialog.accept()

        def no():
            dialog.accept()

        yes_button.clicked.connect(yes)
        no_button.clicked.connect(no)

        label_layout.addWidget(sure_label)
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def room_clicked(self, item):
        self.info_stack.setCurrentIndex(1)
        self.selected_room = item.data(Qt.UserRole)
        self.check_object = 1
        self.room_number.setText(f"Номер: {self.selected_room.number}")
        self.room_type.setText(f"Тип: {self.selected_room.room_type}")
        self.room_password.setText(f"Пароль: {self.selected_room.password}")
        self.room_guests.setText(f"Проживает: {self.selected_room.guest}")

    def change_room(self):
        dialog = QDialog()
        dialog.setWindowTitle("Изменить пароль")
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QHBoxLayout()

        password_label = QLabel("Пароль: ")

        password_line = QLineEdit()

        self.acchange_button = QPushButton("Подтвердить")

        def change():
            if password_line.text().isdigit() and len(password_line.text()) == 4:
                self.selected_room.password = password_line.text()
                self.room_password.setText(f"Пароль: {self.selected_room.password}")
                QMessageBox.information(
                    dialog,
                    "Успех",
                    "Пароль изменен!"
                )
                dialog.accept()
            else:
                QMessageBox.warning(
                    dialog,
                    "Ошибка ввода",
                    "Пароль должен состоять из 4 цифр!"
                )

        self.acchange_button.clicked.connect(change)

        layout.addWidget(password_label)
        layout.addWidget(password_line)
        layout.addWidget(self.acchange_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_room(self):
        dialog = QDialog()
        dialog.setWindowTitle("Добавить комнату")
        dialog.setStyleSheet(DIALOG_STYLE)


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
                    QMessageBox.warning(
                        dialog,
                        "Ошибка",
                        "Комната с таким номером уже есть!"
                    )
                    return
                else:
                    room = Room(number, room_type)
                    room.password = password
                    self.manager.rooms.append(room)
                    item = QListWidgetItem()
                    item.setData(Qt.UserRole, room)
                    self.rooms_list.addItem(item)
                    item.setText(f"{self.rooms_list.count()}: {room.room_type}")
                    QMessageBox.information(
                        dialog,
                        "Успех",
                        "Комната добавлена!"
                    )
                    dialog.accept()
            else:
                QMessageBox.warning(
                    dialog,
                    "Ошибка",
                    "Проверьте правильность введённых данных!"
                )

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


    def delete_room(self):
        dialog = QDialog()
        dialog.setWindowTitle("Удалить")
        dialog.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        yes_button = QPushButton("Да")
        no_button = QPushButton("Нет")

        sure_label = QLabel(f"Вы уверены что хотите удалить {self.selected_room.number} комнату?")

        def yes():
            item = self.rooms_list.currentItem()
            if self.selected_room.guest is None:
                Manager.rooms.remove(self.selected_room)
                self.rooms_list.takeItem(self.rooms_list.row(item))
                self.room_number.setText("")
                self.room_type.setText("")
                self.room_password.setText("")
                self.room_guests.setText("")
                QMessageBox.information(
                    dialog,
                    "Успех",
                    "Комната удалена!"
                )
                dialog.accept()
            else:
                new_room = Manager.find_free_room(self.selected_room.room_type)
                if new_room is None:
                    QMessageBox.warning(
                        dialog,
                        "Ошибка",
                        "Перед удалением этой комнаты, создайте комнату для текущего жителя такого же типа"
                    )
                    dialog.accept()
                elif not new_room is None:
                    homeless = self.selected_room.guest
                    Manager.rooms.remove(self.selected_room)
                    self.rooms_list.takeItem(self.rooms_list.row(item))
                    homeless.room = new_room
                    new_room.guest = homeless
                    self.room_number.setText("")
                    self.room_type.setText("")
                    self.room_password.setText("")
                    self.room_guests.setText("")
                    QMessageBox.information(
                        dialog,
                        "Успех",
                        "Комната удалена!"
                    )
                    dialog.accept()
        def no():
            dialog.accept()

        yes_button.clicked.connect(yes)
        no_button.clicked.connect(no)

        label_layout.addWidget(sure_label)
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()