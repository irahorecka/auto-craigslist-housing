import sys
import qdarkstyle
from PyQt5.QtCore import QThread, QPersistentModelIndex, pyqtSignal
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem
from ui import UiMainWindow


class MainPage(QMainWindow, UiMainWindow):
    """Main page of the application."""

    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainPage()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    widget.show()
    sys.exit(app.exec_())