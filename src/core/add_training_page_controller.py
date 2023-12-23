from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
import re

from src.core.customized_exercises import CustomizedExercises
from src.core.trainees import Trainees
from src.core.workouts import Workouts


class AddTrainingPageController:
    def __init__(self, ui):
        self.ui = ui
        self.list_of_exercises = []
        self.model_exercises = QStandardItemModel()

    def open_add_training_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_training_page)

    def select_trainee_info_combobox(self, trainees):
        selected_index = self.ui.choose_trainee_comboBox.currentIndex()
        selected_trainee_data = trainees[selected_index]
        return Trainees(selected_trainee_data[1],
                        selected_trainee_data[2],
                        selected_trainee_data[3],
                        selected_trainee_data[4],
                        selected_trainee_data[5],
                        selected_trainee_data[6],
                        selected_trainee_data[7],
                        selected_trainee_data[8],
                        selected_trainee_data[9],
                        selected_trainee_data[10],
                        selected_trainee_data[0]
                        )

    def create_workout(self, trainee_id):
        return Workouts(trainee_id,
                        self.ui.name_of_training_lineEdit.text(),
                        str(self.ui.start_date_training_dateEdit.date().year())
                        + "-" + str(self.ui.start_date_training_dateEdit.date().month())
                        + "-" + str(self.ui.start_date_training_dateEdit.date().day()),
                        self.ui.training_desc_lineEdit.toPlainText()
                        )

    def validate_data_add_training_page(self):
        required_fields = [
            self.ui.name_of_exercise_lineEdit.text(),
            self.ui.number_of_sets_lineEdit.text(),
            self.ui.number_of_reps_lineEdit.text(),
        ]
        if any(not field for field in required_fields):
            self.show_popup("Nieprawidłowe dane!")
            return True
        if (not (re.match(r'^\d+$', self.ui.number_of_sets_lineEdit.text())
                 and re.match(r'^\d+$', self.ui.number_of_reps_lineEdit.text()))):
            self.show_popup("Nieprawidłowe dane!")
            return True
        return False

    def add_exercise(self):
        if self.validate_data_add_training_page():
            return
        self.list_of_exercises.append((self.ui.name_of_exercise_lineEdit.text(),
                                       self.ui.number_of_sets_lineEdit.text(),
                                       self.ui.number_of_reps_lineEdit.text(),
                                       self.ui.additional_info_editText.toPlainText()
                                       ), )
        exe_info = QStandardItem(" ".join((self.ui.name_of_exercise_lineEdit.text(),
                                           self.ui.number_of_sets_lineEdit.text(),
                                           self.ui.number_of_reps_lineEdit.text(),
                                           )))
        self.model_exercises.appendRow(exe_info)
        self.ui.exercises_list.setModel(self.model_exercises)

        for line_edit in self.ui.add_training_page.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()
        self.ui.additional_info_editText.setPlainText("")
        print(self.list_of_exercises)

    def add_training(self, db_manager, workout):
        wor_id = workout.add_workout_to_db(db_manager)
        self.list_of_exercises = [(wor_id,) + exe for exe in self.list_of_exercises]
        CustomizedExercises.add_multiple_customized_exercises_to_db(db_manager, self.list_of_exercises)
        self.clear_data()
        # self.ui.exercises_list.setModel(self.model_exercises)


    def clear_data(self):
        self.list_of_exercises = []
        self.model_exercises.clear()
        for line_edit in self.ui.add_training_page.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

        for line_edit in self.ui.add_training_name.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

        self.ui.additional_info_editText.setPlainText("")
        self.ui.training_desc_lineEdit.setPlainText("")

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
