from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox


class AddTrainingNameController:
    def __init__(self, ui):
        self.ui = ui


    def set_trainees_checkbox(self, trainees, trainee):
        for person in trainees:
            self.ui.choose_trainee_comboBox.addItem(f"{person[1]} {person[2]}")
        if trainee.name != 'name':
            self.ui.choose_trainee_comboBox.setCurrentText(f"{trainee.name} {trainee.surname}")
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_training_name)

    def validate_data_add_training_name(self):
        required_fields = [
            self.ui.choose_trainee_comboBox.currentText(),
            self.ui.name_of_training_lineEdit.text(),
            self.ui.start_date_training_dateEdit.date(),
        ]

        if any(not field for field in required_fields):
            self.show_popup("Nieprawidłowe dane!")
            return True
        return False


    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
