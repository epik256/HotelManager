MAIN_STYLE = """
    QMainWindow, QDialog {
        background-color: #202522;
        color: #e5e9e5;
    }

    QLabel {
        color: #e5e9e5;
        font-size: 14px;
    }

    QListWidget {
        background-color: #292f2b;
        color: #e5e9e5;
        border: 1px solid #414a43;
        border-radius: 6px;
        padding: 5px;
    }

    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }

    QListWidget::item:selected {
        background-color: #476b4d;
        color: white;
    }

    QPushButton#deleteButton {
        background-color: #3d6645;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 9px 14px;
    }
    
    QPushButton#deleteButton:hover {
        background-color: #ad4451;
    }
 

    QPushButton#changeButton:hover {
        background-color: #333b8f;
    }

    QPushButton#debitButton:hover {
        background-color: #c7b765;
    }

    QPushButton {
        background-color: #3d6645;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 9px 14px;
    }

    QPushButton:hover {
        background-color: #507f59;
    }

    QLineEdit, QComboBox {
        background-color: #292f2b;
        color: white;
        border: 1px solid #414a43;
        border-radius: 5px;
        padding: 6px;
    }

"""


DIALOG_STYLE = """
    QDialog {
        background-color: #202522;
    }
    
    QLabel {
        color: #e5e9e5;
        font-size: 14px;
    }


    QPushButton#noButton:hover {
        background-color: #ad4451;
    }

    QPushButton {
        background-color: #3d6645;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
    }
    
    QPushButton:hover {
        background-color: #507f59;
    }
    
    QLineEdit, QComboBox {
        background-color: #292f2b;
        color: white;
        border: 1px solid #414a43;
        border-radius: 5px;
        padding: 7px;
    }
    
    QComboBox QAbstractItemView { show-decoration-selected: 1; }
    
    QComboBox QAbstractItemView {
        background-color: #292f2b;
        color: white;
    }
    
    QComboBox QAbstractItemView::item:hover {
                    background-color: white;
    }

"""
