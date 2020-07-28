import os
import sys
import qdarkstyle
from PyQt5.QtCore import QThread, QPersistentModelIndex, pyqtSignal
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem
from ui import UiMainWindow
from utils import get_static_file


class MainPage(QMainWindow, UiMainWindow):
    """Main page of the application."""

    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi(self)

        # set default gmail and password if in local environment
        self.set_default_email()

        # set items for QComboBox
        qcombo_box = get_static_file.qcombo_box()
        self.min_bathrooms.addItems(qcombo_box.get("min_bathrooms"))
        self.max_bathrooms.addItems(qcombo_box.get("max_bathrooms"))
        self.min_bedrooms.addItems(qcombo_box.get("min_bedrooms"))
        self.max_bedrooms.addItems(qcombo_box.get("max_bedrooms"))

        # add functionality to subscribe & cancel buttons
        self.subscribe.clicked.connect
        self.cancel.clicked.connect(self.close)

        self.apts_housing.setChecked(True)
        self.apts_housing.clicked.connect(self.show_bathrooms_bedrooms)
        # self.apts_housing.clicked.connect(self.process_apts_housing)
        self.rooms_shares.clicked.connect(self.hide_bathrooms_bedrooms)
        # self.rooms_shares.clicked.connect(self.process_rooms_shares)

    def set_default_email(self):
        gmail = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASS")
        # TODO: decide if && statement should be used
        if gmail:
            self.gmail.setText(gmail)
        if password:
            self.password.setText(password)

    def hide_bathrooms_bedrooms(self):
        self.bathrooms_label.hide()
        self.bedrooms_label.hide()
        self.min_bathrooms.hide()
        self.max_bathrooms.hide()
        self.min_bedrooms.hide()
        self.max_bedrooms.hide()

    def show_bathrooms_bedrooms(self):
        self.bathrooms_label.show()
        self.bedrooms_label.show()
        self.min_bathrooms.show()
        self.max_bathrooms.show()
        self.min_bedrooms.show()
        self.max_bedrooms.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainPage()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    widget.show()
    sys.exit(app.exec_())
