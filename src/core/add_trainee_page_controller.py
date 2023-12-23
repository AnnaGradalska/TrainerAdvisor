from PyQt5.QtWidgets import QMessageBox

from trainees import Trainees
import re


class AddTraineePageController:
    def __init__(self, ui):
        self.ui = ui

    def add_trainee(self, db_manager):
        print("add_trainee")
        if (not (self.validate_data_add_trainee())):
            self.show_popup("Nieprawidłowe dane! Wypełnij formularz poprawnie.")
            return
        trainee = Trainees(self.ui.name_lineEdit.text(),
                           self.ui.surname_lineEdit.text(),
                           self.ui.email_lineEdit.text(),
                           str(self.ui.date_of_birth_dateEdit.date().year())
                           + "-" + str(self.ui.date_of_birth_dateEdit.date().month())
                           + "-" + str(self.ui.date_of_birth_dateEdit.date().day()),
                           self.ui.phone_lineEdit.text(),
                           str(self.ui.add_start_date_training_dateEdit.date().year())
                           + "-" + str(self.ui.add_start_date_training_dateEdit.date().month())
                           + "-" + str(self.ui.add_start_date_training_dateEdit.date().day()),
                           self.ui.weight_lineEdit.text(),
                           self.ui.deadlift_lineEdit.text(),
                           self.ui.benchpress_lineEdit.text(),
                           self.ui.squat_lineEdit.text()
                           )

        trainee.add_trainee_to_db(db_manager)
        print("Dodano")
        return trainee

    def validate_data_add_trainee(self):
        required_fields = [
            self.ui.name_lineEdit.text(),
            self.ui.surname_lineEdit.text(),
            self.ui.email_lineEdit.text(),
            self.ui.phone_lineEdit.text(),
            self.ui.weight_lineEdit.text(),
            self.ui.deadlift_lineEdit.text(),
            self.ui.benchpress_lineEdit.text(),
            self.ui.squat_lineEdit.text()
        ]
        if any(not field for field in required_fields):
            return False
        if not (re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.ui.email_lineEdit.text())):
            return False
        if not (re.match(r'^\d{9}$', self.ui.phone_lineEdit.text())):
            return False

        return True

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
