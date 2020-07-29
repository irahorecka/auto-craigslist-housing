import os
import smtplib
import ssl
import sys
import time
from socket import gaierror
import qdarkstyle
from PyQt5.QtCore import QThread, QPersistentModelIndex, pyqtSignal
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem
import craigslist_housing
from ui import UiMainWindow
import utils


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
        self.rooms_shares.clicked.connect(self.hide_bathrooms_bedrooms)
        # Set items for QComboBox
        qcombo_box = utils.qcombo_box()
        self.min_bathrooms.addItems(qcombo_box.get("min_bathrooms"))
        self.max_bathrooms.addItems(qcombo_box.get("max_bathrooms"))
        self.min_bedrooms.addItems(qcombo_box.get("min_bedrooms"))
        self.max_bedrooms.addItems(qcombo_box.get("max_bedrooms"))

        # SUBSCRIBE / CANCEL
        self.subscribe.clicked.connect(self.hide_warning_labels)
        self.subscribe.clicked.connect(self.submit_form)
        self.cancel.clicked.connect(self.close)

    def submit_form(self):
        validation = [
            validate_func()
            for validate_func in [
                self.validate_sender,
                self.validate_receiver,
                self.validate_email_login,
            ]
        ]
        if all(validation):
            print("yerrrt")  # works
            self.run_app()

    def validate_sender(self):
        validation = True
        if not self.verify_text(self.gmail):
            self.gmail_label_warn.show()
            validation = False
        if not self.verify_text(self.password):
            self.password_label_warn.show()
            validation = False

        return validation

    def validate_receiver(self):
        if not self.verify_text(self.send_to):
            self.send_to_label_warn.show()
            return False

        return True

    def validate_email_login(self):
        ssl_context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
                server.login(self.get_text(self.gmail), self.get_text(self.password))
                return True
        except (
            smtplib.SMTPAuthenticationError,
            TypeError,
        ):  # TypeError -- empty credentials
            self.show_gmail_failure("Invalid Gmail credentials")
        except gaierror:
            self.show_gmail_failure("No internet connection")

        return False

    def run_app(self):
        craigslist_param = {
            "housing_type": "roo",
            "gmail_user": self.gmail,
            "gmail_pass": self.password,
            "email_recipient": self.send_to,  # type list
            "email_subject": self.subject,
            "email_message": self.message,
            "miles": self.get_int(self.miles),
            "zipcode": self.get_int(self.miles),
            "min_price": self.get_int(self.min_price),
            "max_price": self.get_int(self.max_price),
            "min_sqft": self.get_int(self.min_sqft),
            "max_sqft": self.get_int(self.max_sqft),
        }
        if self.apts_housing.isChecked():
            additional_param = {
                "housing_type": "apa",
                "min_bathrooms": self.get_int(self.min_bathrooms),
                "max_bathrooms": self.get_int(self.max_bathrooms),
                "min_bedrooms": self.get_int(self.min_bedrooms),
                "max_bedrooms": self.get_int(self.max_bedrooms),
            }
            craigslist_param = {**craigslist_param, **additional_param}

        if all(craigslist_param[param] for param in ["miles", "zipcode"]):
            # utils.set_mile_and_zipcode(craigslist_param)
            posts = craigslist_housing.scrape(
                housing_category=craigslist_param.get("housing_type"), geotagged=False
            )
            print("hit1")
            filtered_posts = craigslist_housing.filter_posts(posts, craigslist_param)
            print("hit2")
            new_posts = craigslist_housing.get_new_posts(filtered_posts)
            print("hit3")
            utils.write_email(new_posts)
            print("hit4")

    def set_default_email(self):
        """set default gmail and password if in local environment"""
        gmail = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASS")
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

    def show_gmail_failure(self, message):
        self.gmail_label_fail.setText(message)
        self.gmail_label_fail.setStyleSheet("color:#fc0107;")
        self.gmail_label_fail.show()

    def get_int(self, text):
        try:
            text = float(self.get_text(text))
            try:
                return int(text)
            except ValueError:
                return None
        except ValueError:
            return None

    @staticmethod
    def get_text(text):
        """Get text of cell value, if empty return empty str."""
        try:
            return text.text()
        except AttributeError:
            return ""

    @staticmethod
    def verify_text(text):
        return bool(text.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainPage()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    widget.show()
    sys.exit(app.exec_())
