import os
import smtplib
import ssl
import sys
from socket import gaierror

from numpy.lib.arraysetops import isin
from utils.get_static_file import search_filters
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
    QLabel,
    QListWidgetItem,
)
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

        self.buildExamplePopup()

        # CRAIGSLIST PARAMETERS
        self.apts_housing.setChecked(True)
        self.apts_housing.clicked.connect(self.show_bedrooms)
        self.rooms_shares.clicked.connect(self.hide_bedrooms)
        # Set items for QComboBox
        qcombo_box = utils.qcombo_box()
        self.min_bedrooms.addItems(qcombo_box.get("min_bedrooms"))
        self.max_bedrooms.addItems(qcombo_box.get("max_bedrooms"))

        # SUBSCRIBE / CANCEL
        self.subscribe.clicked.connect(self.hide_warning_labels)
        self.subscribe.clicked.connect(self.submit_form)
        self.cancel.clicked.connect(self.close)

    def submit_form(self):
        """Submit application form (email and housing info)
        for validation and, if valid, execution."""
        validation = [
            validate_func()
            for validate_func in [
                self.validate_sender,
                self.validate_receiver,
                self.validate_email_login,
            ]
        ]
        if all(validation):
            self.run_app()

    def validate_sender(self):
        """Validate Gmail account and password (run 1) by
        verifying a non-empty QLineEdit object."""
        validation = True
        if not self.verify_text(self.gmail):
            self.gmail_label_warn.show()
            validation = False
        if not self.verify_text(self.password):
            self.password_label_warn.show()
            validation = False

        return validation

    def validate_receiver(self):
        """Validate email recipient by verifying a non-empty QLineEdit
        object."""
        if not self.verify_text(self.send_to):
            self.send_to_label_warn.show()
            return False

        return True

    def validate_email_login(self):
        """Validate Gmail account and password (run 2) by
        verifying email and password by login simulation."""
        ssl_context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
                server.login(self.get_text(self.gmail), self.get_text(self.password))
                return True
        except (
            smtplib.SMTPAuthenticationError,
            TypeError,
        ):  # TypeError -- empty credentials
            self.show_general_message("Invalid Gmail credentials")
        except gaierror:
            self.show_general_message("No internet connection")

        return False

    def run_app(self):
        """Process frontend information to be parsed by backend.
        Send information as dictionary object."""
        craigslist_param = {
            "housing_type": "roo",
            "gmail_user": self.get_text(self.gmail),
            "gmail_pass": self.get_text(self.password),
            "email_recipient": [
                recip.strip(" ") for recip in self.get_text(self.send_to).split(";")
            ],  # type list
            "email_subject": self.get_text(self.subject),
            "email_message": self.get_text_box(self.message),  # get text from QTextBox
            "miles": self.get_int(self.miles),
            "zipcode": self.get_int(self.zipcode),
            "min_price": self.get_int(self.min_price),
            "max_price": self.get_int(self.max_price),
            "min_sqft": self.get_int(self.min_sqft),
            "max_sqft": self.get_int(self.max_sqft),
        }
        if self.apts_housing.isChecked():
            # add additional parameters if apts & housing is selected
            additional_param = {
                "housing_type": "apa",
                "min_bedrooms": self.get_qcombo_int(self.min_bedrooms),
                "max_bedrooms": self.get_qcombo_int(self.max_bedrooms),
            }
            craigslist_param = {**craigslist_param, **additional_param}

        # validate zipcode and miles are populated in craigslist_param
        if all(craigslist_param[param] for param in ["miles", "zipcode"]):
            utils.set_miles_and_zipcode(craigslist_param)

            self.subscribe.setEnabled(False)
            self.show_general_message("Loading...", failure=False)
            self.load_results = LoadingResults(craigslist_param)
            self.load_results.loadFinished.connect(self.show_general_message)
            self.load_results.start()

    def set_default_email(self):
        """set default gmail and password if in local environment"""
        gmail = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASS")
        if gmail:
            self.gmail.setText(gmail)
        if password:
            self.password.setText(password)

    def hide_bedrooms(self):
        """Hide bedrooms label, min and max bedrooms."""
        self.bedrooms_label.hide()
        self.min_bedrooms.hide()
        self.max_bedrooms.hide()

    def show_bedrooms(self):
        """Show bedrooms label, min and max bedrooms."""
        self.bedrooms_label.show()
        self.min_bedrooms.show()
        self.max_bedrooms.show()

    def hide_warning_labels(self):
        """Hide all warning labels."""
        self.gmail_label_warn.hide()
        self.general_label.hide()
        self.password_label_warn.hide()
        self.send_to_label_warn.hide()

    def show_general_message(self, message, failure=True):
        """Show general failure message above Submit button.
        Error message will be message param."""
        if isinstance(message, tuple):
            message = "".join(message)
            self.subscribe.setEnabled(True)
        self.general_label.setText(message)
        if failure:
            self.general_label.setStyleSheet("color:#fc0107;")
        else:
            self.general_label.setStyleSheet("color:#000000;")
        self.general_label.show()

    def get_int(self, text):
        """Get integer from string."""
        try:
            text = float(self.get_text(text))
            try:
                return int(text)
            except ValueError:
                return None
        except ValueError:
            return None

    @pyqtSlot(QListWidgetItem)
    def buildExamplePopup(self):
        self.exPopup = examplePopup(self)
        self.exPopup.setGeometry(100, 200, 100, 100)
        self.exPopup.show()

    # @staticmethod
    # def subscribe_popup():
    #     """Get user to select recurring subscription."""
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Subscription")
    #     msg.setText("Input recurring hours for Craigslist notifications.\nPress cancel to exit.")
    #     msg.addButton(QPushButton("Subscribe"), QMessageBox.YesRole)
    #     msg.addButton(QPushButton("Cancel"), QMessageBox.NoRole)
    #     msg.setText('to select click "show details"')
    #     msg.setTextInteractionFlags(Qt.NoTextInteraction) # (QtCore.Qt.TextSelectableByMouse)
    #     msg.setDetailedText('line 1\nline 2\nline 3')
    #     # TODO: enable closing feature on window close button
    #     upload_type_bool = msg.exec_()
    #     if not upload_type_bool:
    #         return True
    #     return False, 0

    @staticmethod
    def get_qcombo_int(text):
        """Get text from QComboBox object."""
        try:
            return int(str(text.currentText()))
        except ValueError:
            return None

    @staticmethod
    def get_text_box(text):
        """Get text from QTextEdit object."""
        try:
            return text.toPlainText()
        except AttributeError:
            return ""

    @staticmethod
    def get_text(text):
        """Get text of cell value, if empty return empty str."""
        try:
            return text.text()
        except AttributeError:
            return ""

    @staticmethod
    def verify_text(text):
        """Verify non-empty QLineEdit object."""
        try:
            return bool(text.text())
        except AttributeError:
            return False


class examplePopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.name = "Test"
        self.label = QLabel("Woohoo", self)


class LoadingResults(QThread):
    # TODO : Hide exception thrown by sqlite3 for termination of thread.
    """Load results when subscribe button is clicked."""

    loadFinished = pyqtSignal(tuple, bool)

    def __init__(self, search_param, parent=None):
        QThread.__init__(self, parent)
        self.search_param = search_param
        self.load_failed = False
        self.message = "Load complete."

    def run(self):
        try:
            posts = craigslist_housing.scrape(
                housing_category=self.search_param.get("housing_type"), geotagged=False
            )
            if posts is None:
                self.show_general_message("Could not get posts. Try again.")
                return
            filtered_posts = craigslist_housing.filter_posts(posts, self.search_param)
            new_posts = craigslist_housing.get_new_posts(filtered_posts)
            utils.write_email(new_posts, self.search_param)
        except Exception as e:  # poor error catching -- amend later
            print(e)
            self.load_failed = True
            self.message = "Load failed."

        self.loadFinished.emit(
            tuple(self.message), self.load_failed
        )  # cannot emit str?


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec_())
