import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from src.gui.demo4_praca_inzynierska import Ui_MainWindow
from button_controler import ButtonController




class MainWindow:

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

        self.button_controler = ButtonController(self.ui, self.main_win)


    def show(self):
        self.main_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())