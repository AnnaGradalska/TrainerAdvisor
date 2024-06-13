from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from src.core.database_handlers.personal_records import PersonalRecords
from src.core.database_handlers.trainees import Trainees
import re



class AddPersonalRecordsPageController:
    def __init__(self, ui, db_manager):
        self.ui = ui
        self.db_manager = db_manager

    def open_add_personal_records(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_personal_records_page)

    def select_trainee_info_combobox(self, trainees):
        selected_index = self.ui.choose_trainee_comboBox_records.currentIndex()
        selected_trainee_data = trainees[selected_index]
        return Trainees(selected_trainee_data[1],
                        selected_trainee_data[2],
                        selected_trainee_data[3],
                        selected_trainee_data[4],
                        selected_trainee_data[5],
                        selected_trainee_data[6],
                        selected_trainee_data[7],
                        selected_trainee_data[0]
                        )

    def add_personal_record_to_db(self, trainee_id):
        personal_record = PersonalRecords(trainee_id,
                                          self.ui.squat_records.text(),
                                          self.ui.bench_press_records.text(),
                                          self.ui.deadlift_records.text(),
                                          str(self.ui.date_records.date().year())
                                          + "-" + str(self.ui.date_records.date().month())
                                          + "-" + str(self.ui.date_records.date().day())
                                          )
        result = personal_record.add_personal_record_to_db(self.db_manager)
        if not result:
            return

    def set_trainees_checkbox(self, trainees, trainee):
        for person in trainees:
            self.ui.choose_trainee_comboBox_records.addItem(f"{person[1]} {person[2]}")
        if trainee.name != 'name':
            self.ui.choose_trainee_comboBox_records.setCurrentText(f"{trainee.name} {trainee.surname}")
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_personal_records_page)

    def validate_data_add_training_name(self):
        required_fields = [
            self.ui.choose_trainee_comboBox_records.currentText(),
            self.ui.squat_records.text(),
            self.ui.bench_press_records.text(),
            self.ui.deadlift_records.text(),
            self.ui.start_date_training_dateEdit.date(),
        ]

        if any(not field for field in required_fields):
            self.show_popup("Nieprawidłowe dane!")
            return True

        if (not (re.match(r'^\d+$', self.ui.squat_records.text())
                 and re.match(r'^\d+$', self.ui.bench_press_records.text())
                 and re.match(r'^\d+$', self.ui.deadlift_records.text()))):
            self.show_popup("Nieprawidłowe dane!")
            return True
        return False

    def clear_data(self):
        for line_edit in self.ui.add_personal_records_page.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()