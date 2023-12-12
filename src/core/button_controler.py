from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from src.core.customized_exercises import CustomizedExercises
from src.core.trainees import Trainees
from src.core.workouts import Workouts
from src.data.database_manager import DatabaseManager
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from main_page_controller import MainPageController
from navbar_controller import NavbarController
import re


class ButtonController:

    def __init__(self, ui, main_win):

        self.model = QStandardItemModel()
        self.ui = ui
        self.main_win = main_win
        # navbar_controller
        self.navbar_controller = NavbarController(self.ui)

        # mainPage
        self.main_page_controller = MainPageController(self.ui)
        self.connect_buttons()
        self.db_manager = DatabaseManager()

        self.trainee = Trainees('name', 'surname', 'email', '2000-01-01', 999999999, 'training_start_date', 99, 99, 99,
                                99)
        self.table_of_trainees = []
        self.refresh_list_trainees()
        self.num = 99
        self.list_of_exercises = []
        self.model_exercises = QStandardItemModel()

        print(self.trainee.select_all(self.db_manager))

        self.refresh_list_trainees()

    def connect_buttons(self):
        # navbuttons
        self.ui.menu_navbutton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.main_page))
        self.ui.list_of_trainees_navbutton.clicked.connect(lambda: self.navbar_controller.open_page(self.ui.list_of_trainees_page))
        self.ui.add_training_navbutton.clicked.connect(lambda: self.navbar_controller.open_page(self.ui.add_training_name))
        self.ui.generate_report_navbutton.clicked.connect(
            lambda: self.navbar_controller.open_page(self.ui.generate_report_page))
        # menu_buttons
        self.ui.list_of_trainees_menu_button.clicked.connect(self.main_page_controller.open_list_of_trainees_page)
        self.ui.add_trainee_menu_button.clicked.connect(self.open_add_training_name)
        self.ui.generate_report_menu_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.generate_report_page))
        # list_of_trainees_page
        self.ui.add_trainee_list_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.add_trainee_page))
        self.ui.refresh_button.clicked.connect(self.refresh_list_trainees)
        self.ui.list_of_trainees.clicked.connect(self.open_trainee_page)
        # add_trainee_page
        self.ui.add_trainee_button.clicked.connect(self.add_trainee)
        # view_trainee_page
        self.ui.add_training_trainee_button.clicked.connect(self.open_add_training_name)
        self.ui.show_training_trainee_button.clicked.connect(self.open_view_training_page)
        self.ui.delete_trainee_button.clicked.connect(self.delete_trainee)
        # add_training_name
        self.ui.move_to_add_exercises_button.clicked.connect(self.create_training)
        # add_training_page
        self.ui.add_next_excercise_button.clicked.connect(self.add_exercise)
        self.ui.add_training_button.clicked.connect(self.add_training)
        # generate_report_page
        self.ui.add_photos_button.clicked.connect(self.choose_picture)

        # self.ui.add_trainee_list_button(self.ui.stackedWidget.setCurrentWidget(self.ui.add_trainee_page))
        # add_training_name

    def add_trainee(self):
        if (not (self.validate_data_add_trainee())):
            self.show_popup("Nieprawidłowe dane! Wypełnij formularz poprawnie.")
            return
        self.trainee = Trainees(self.ui.name_lineEdit.text(),
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

        self.trainee.add_trainee_to_db(self.db_manager)
        # połączyć z open_trainee_page
        self.set_values_on_trainees_page()
        self.ui.stackedWidget.setCurrentWidget(self.ui.view_trainee_page)

    # def open_list_of_trainees_page(self):
    #     self.ui.stackedWidget.setCurrentWidget(self.ui.list_of_trainees_page)

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

    # opis opcjonalny
    def validate_data_add_training_name(self):
        required_fields = [
            self.ui.choose_trainee_comboBox.currentText(),
            self.ui.name_of_training_lineEdit.text(),
            self.ui.start_date_training_dateEdit.date(),
        ]

        if any(not field for field in required_fields):
            return False
        return True

    def validate_data_add_training_page(self):
        required_fields = [
            self.ui.name_of_exercise_lineEdit.text(),
            self.ui.number_of_sets_lineEdit.text(),
            self.ui.number_of_reps_lineEdit.text(),
        ]
        if any(not field for field in required_fields):
            return False
        if (not (re.match(r'^\d+$', self.ui.number_of_sets_lineEdit.text())
                 and re.match(r'^\d+$', self.ui.number_of_reps_lineEdit.text()))):
            return False
        return True

    def open_trainee_page(self):
        selected_index = self.ui.list_of_trainees.currentIndex().row()
        selected_trainee_data = self.table_of_trainees[selected_index]
        self.trainee = Trainees(selected_trainee_data[1],
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
        self.set_values_on_trainees_page()
        self.ui.stackedWidget.setCurrentWidget(self.ui.view_trainee_page)

    def set_values_on_trainees_page(self):
        self.ui.name_surname_dblabel.setText(self.trainee.name + " " + self.trainee.surname)
        self.ui.date_of_birth_label_dblabel.setText(self.trainee.date_of_birth)
        self.ui.email_dblabel.setText(self.trainee.email)
        self.ui.phone_dblabel.setText(self.trainee.phone)
        self.ui.weight_dblabel.setText(str(self.trainee.weight))
        self.ui.start_date_training_db_label.setText(str(self.trainee.training_start_date))
        self.ui.squat_dblabel.setText(str(self.trainee.squat))
        self.ui.benchpress_dblabel.setText(str(self.trainee.benchpress))
        self.ui.deadlift_dblabel.setText(str(self.trainee.deadlift))

    def refresh_list_trainees(self):
        self.model.removeRows(0, self.model.rowCount())
        self.table_of_trainees = self.trainee.select_all(self.db_manager)

        for record in self.table_of_trainees:
            item = QStandardItem(" ".join((record[1], record[2])))
            self.model.appendRow(item)

        self.ui.list_of_trainees.setModel(self.model)

    def open_add_training_name(self):
        self.refresh_list_trainees()
        for person in self.table_of_trainees:
            self.ui.choose_trainee_comboBox.addItem(f"{person[1]} {person[2]}")
        if self.trainee.name != 'name':
            self.ui.choose_trainee_comboBox.setCurrentText(f"{self.trainee.name} {self.trainee.surname}")
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_training_name)

    def create_training(self):
        # dodać opcje w przypadku zmienienia w combobox podopiecznego
        if (not(self.validate_data_add_training_name())):
            self.show_popup("Nieprawidłowe dane!")
            return
        selected_index = self.ui.choose_trainee_comboBox.currentIndex()
        selected_trainee_data = self.table_of_trainees[selected_index]
        self.trainee = Trainees(selected_trainee_data[1],
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

        self.list_of_exercises = []
        self.workout = Workouts(self.trainee.id,
                                self.ui.name_of_training_lineEdit.text(),
                                str(self.ui.start_date_training_dateEdit.date().year())
                                + "-" + str(self.ui.start_date_training_dateEdit.date().month())
                                + "-" + str(self.ui.start_date_training_dateEdit.date().day()),
                                self.ui.training_desc_lineEdit.toPlainText()
                                )
        self.open_add_training_page()

    def open_add_training_page(self):
        # wróć do create_training
        self.ui.stackedWidget.setCurrentWidget(self.ui.add_training_page)

    # pamiętaj o wyzerowaniu listy przy dodawaniu treningu
    def add_exercise(self):
        if not(self.validate_data_add_training_page()):
            self.show_popup("Nieprawidłowe dane!")
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

        # for line_edit in self.ui.add_training_page.findChildren(QtWidgets.QLineEdit):
        #     line_edit.clear()
        self.ui.additional_info_editText.setPlainText("")

    def add_training(self):
        wor_id = self.workout.add_workout_to_db(self.db_manager)
        self.list_of_exercises = [(wor_id,) + exe for exe in self.list_of_exercises]
        CustomizedExercises.add_multiple_customized_exercises_to_db(self.db_manager, self.list_of_exercises)
        # wyczyść po dodaniu treningu
        self.list_of_exercises = []
        self.model_exercises.clear()
        # self.ui.exercises_list.setModel(self.model_exercises)

        for line_edit in self.ui.add_training_page.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

        for line_edit in self.ui.add_training_name.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

        self.ui.additional_info_editText.setPlainText("")
        self.ui.training_desc_lineEdit.setPlainText("")

        self.open_view_training_page()

    def open_view_training_page(self):
        print("wejscie")
        workouts = self.trainee.select_all_trainings(self)
        workouts = [i[0] for i in workouts]
        print(workouts)
        customized_exe = CustomizedExercises("none", "none", "none", "none", "none")
        exercises = customized_exe.get_customized_exercises_for_trainee(workouts)
        print(exercises)
        print(self.workout.select_all(self.db_manager))

        # Grupowanie ćwiczeń według numeru treningu
        grouped_exercises = {}
        for exercise in exercises:
            training_number = exercise[2]
            if training_number not in grouped_exercises:
                grouped_exercises[training_number] = []
            grouped_exercises[training_number].append(exercise)

        # Dodawanie danych do tabeli
        row = 0
        for training_number, exercises_data in grouped_exercises.items():
            for exercise in exercises_data:
                data_to_display = [exercise[i] for i in [1, 3, 4, 5]]
                for col, data in enumerate(data_to_display):
                    item = QTableWidgetItem(str(data))
                    self.ui.training_table.setItem(row, col, item)
                row += 1

        self.ui.stackedWidget.setCurrentWidget(self.ui.view_training_page)

    def choose_picture(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        paths_to_photos, _ = QFileDialog.getOpenFileNames(self.main_win, "Open File", "C:\\",
                                                          "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)

        if len(paths_to_photos) != 5:
            self.show_popup("Wybierz dokładnie 5 zdjęć!")
            return

        if paths_to_photos:
            for path in paths_to_photos:
                print(path)

    def show_popup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()

    def delete_trainee(self):
        self.trainee.delete_trainee_from_db(self.db_manager)
        print("usunięto")
        self.refresh_list_trainees()
        self.main_page_controller.open_list_of_trainees_page()
