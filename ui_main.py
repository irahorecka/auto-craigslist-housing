import os
import smtplib
import ssl
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

        # DEFAULT PARAMETERS
        self.set_default_email()
        self.hide_warning_labels()

        # CRAIGSLIST PARAMETERS
        self.apts_housing.setChecked(True)
        self.apts_housing.clicked.connect(self.show_bathrooms_bedrooms)
        # self.apts_housing.clicked.connect(self.process_apts_housing)
        self.rooms_shares.clicked.connect(self.hide_bathrooms_bedrooms)
        # self.rooms_shares.clicked.connect(self.process_rooms_shares)
        # set items for QComboBox
        qcombo_box = get_static_file.qcombo_box()
        self.min_bathrooms.addItems(qcombo_box.get("min_bathrooms"))
        self.max_bathrooms.addItems(qcombo_box.get("max_bathrooms"))
        self.min_bedrooms.addItems(qcombo_box.get("min_bedrooms"))
        self.max_bedrooms.addItems(qcombo_box.get("max_bedrooms"))

        # SUBSCRIBE / CANCEL
        self.subscribe.clicked.connect(self.hide_warning_labels)
        self.subscribe.clicked.connect(self.submit_form)
        self.cancel.clicked.connect(self.close)

    def submit_form(self):
        if (
            all(valid() for valid in [self.validate_send_from, self.validate_send_to])
            and self.verify_email_login()
        ):
            print("yerrrt")  # works
            # self.build_email_body()
            # self.run_app()

    def validate_send_from(self):
        validation = True
        if not self.verify_text(self.gmail):
            self.gmail_label_warn.show()
            validation = False
        if not self.verify_text(self.password):
            self.password_label_warn.show()
            validation = False

        return validation

    def validate_send_to(self):
        if not self.verify_text(self.send_to):
            self.send_to_label_warn.show()
            return False

        return True

    def verify_email_login(self):
        ssl_context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
                server.login(self.get_text(self.gmail), self.get_text(self.password))
                return True
        except smtplib.SMTPAuthenticationError:
            self.gmail_label_fail.show()
            return False

    def build_email_body(self):
        pass

    def set_default_email(self):
        """set default gmail and password if in local environment"""
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

    def hide_warning_labels(self):
        self.gmail_label_warn.hide()
        self.gmail_label_fail.hide()
        self.password_label_warn.hide()
        self.send_to_label_warn.hide()

    @staticmethod
    def verify_text(text):
        return bool(text.text())

    @staticmethod
    def get_text(text):
        """Get text of cell value, if empty return empty str."""
        try:
            return text.text()
        except AttributeError:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainPage()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    widget.show()
    sys.exit(app.exec_())
