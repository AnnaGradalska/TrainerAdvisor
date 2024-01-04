from PyQt5.QtWidgets import QMessageBox

from src.core.controllers.add_training_name_controller import AddTrainingNameController
from src.core.controllers.add_training_page_controller import AddTrainingPageController
from src.core.controllers.generate_report_page_controller import GenerateReportPageController
from src.core.database_handlers.trainees import Trainees
from src.core.controllers.view_training_page_controller import ViewTrainingPageController
from src.core.database_handlers.workouts import Workouts
from src.data.database_manager import DatabaseManager
from PyQt5.QtGui import QStandardItemModel
from menu_page_controller import MenuPageController
from navbar_controller import NavbarController
from list_of_trainees_controller import ListOfTraineesController
from add_trainee_page_controller import AddTraineePageController
from view_trainee_page_controller import ViewTraineePageController


class ButtonController:

    def __init__(self, ui, main_win):
        self.ui = ui
        self.main_win = main_win
        self.button_event_mappings = {}
        self.db_manager = DatabaseManager()
        self.navbar_controller = NavbarController(self.ui)
        self.menu_page_controller = MenuPageController(self.ui)
        self.list_of_trainees_controller = ListOfTraineesController(self.ui)
        self.add_trainee_page_controller = AddTraineePageController(self.ui)
        self.view_trainee_page_controller = ViewTraineePageController(self.ui)
        self.add_training_name_controller = AddTrainingNameController(self.ui)
        self.add_training_page_controller = AddTrainingPageController(self.ui)
        self.view_training_page_controller = ViewTrainingPageController(self.ui, self.db_manager)
        self.generate_report_page_controller = GenerateReportPageController(self.main_win, self.ui)
        self.connect_buttons()

        self.trainee = Trainees('name', 'surname', 'email', '2000-01-01', 999999999, 'training_start_date', 99, 99, 99,
                                99)
        self.workout = Workouts(0, 'workout', '2000-01-01')
        self.table_of_trainees = self.list_of_trainees_controller.refresh_list_trainees(self.db_manager)
        self.num = 99
        self.list_of_exercises = []
        self.model_exercises = QStandardItemModel()

        print(self.trainee.select_all(self.db_manager))

    def map_button_event(self, button, event_handler):
        self.button_event_mappings[button] = event_handler
        print(self.button_event_mappings)

    def handle_button_event(self, button):
        try:
            for event_handler in self.button_event_mappings[button]:
                event_handler()
        except Exception as e:
            ButtonController.show_popup(f"Błąd: {e}. Nie można dodać użytkownika.")

    def add_trainee_get_value(self):
        result = self.add_trainee_page_controller.add_trainee(self.db_manager)
        if not result:
            return False
        self.trainee = result

    def connect_buttons(self):
        self.connect_nav_buttons()
        self.connect_menu_buttons()
        self.connect_list_of_trainees_page_buttons()
        self.connect_view_trainee_page_buttons()
        self.connect_add_training_name_buttons()
        self.connect_add_training_page_buttons()
        self.connect_generate_report_page_buttons()
        self.connect_add_trainee_page_buttons()
        self.connect_view_training_page_buttons()
        self.connect_report_page_buttons()
        self.connect_report_page_controller()

    def connect_nav_buttons(self):
        self.ui.menu_navbutton.clicked.connect(
            lambda: self.navbar_controller.open_page(self.ui.main_page))
        self.ui.list_of_trainees_navbutton.clicked.connect(
            lambda: self.navbar_controller.open_page(self.ui.list_of_trainees_page))
        self.ui.add_training_navbutton.clicked.connect(
            lambda: self.navbar_controller.open_page(self.ui.add_training_name))
        self.ui.generate_report_navbutton.clicked.connect(
            lambda: self.navbar_controller.open_page(self.ui.generate_report_page))

    def connect_menu_buttons(self):
        self.ui.list_of_trainees_menu_button.clicked.connect(
            lambda: self.menu_page_controller.open_page(self.ui.list_of_trainees_page))
        self.ui.add_trainee_menu_button.clicked.connect(
            lambda: self.menu_page_controller.open_page(self.ui.add_trainee_page))
        self.ui.generate_report_menu_button.clicked.connect(
            lambda: self.menu_page_controller.open_page(self.ui.generate_report_page))

    def connect_list_of_trainees_page_buttons(self):
        self.ui.add_trainee_list_button.clicked.connect(
            lambda: self.list_of_trainees_controller.open_page(self.ui.add_trainee_page))
        self.ui.refresh_button.clicked.connect(
            lambda: self.list_of_trainees_controller.refresh_list_trainees(self.db_manager))
        self.ui.list_of_trainees.clicked.connect(self.open_trainee_page)

    def connect_view_trainee_page_buttons(self):
        self.ui.add_training_trainee_button.clicked.connect(self.open_add_training_name)
        self.ui.show_training_trainee_button.clicked.connect(
            lambda: self.view_training_page_controller.open_view_training_page(self.trainee, self.workout))
        self.ui.delete_trainee_button.clicked.connect(
            lambda: self.view_trainee_page_controller.delete_trainee(
                self.db_manager, self.trainee, self.list_of_trainees_controller, self.menu_page_controller)
        )

    def connect_add_training_name_buttons(self):
        self.ui.move_to_add_exercises_button.clicked.connect(self.create_training)

    def connect_add_training_page_buttons(self):
        self.ui.add_next_excercise_button.clicked.connect(self.add_exercises)
        self.ui.add_training_button.clicked.connect(self.add_training)

    def connect_generate_report_page_buttons(self):
        self.ui.add_film_button.clicked.connect(self.generate_report_page_controller.open_film)
        self.ui.add_photos_button.clicked.connect(self.generate_report_page_controller.open_photos)
        self.ui.render_film_button.clicked.connect(self.generate_report_page_controller.generate_report_film)
        self.ui.render_photos_button.clicked.connect(self.generate_report_page_controller.generate_report_photos)
        self.ui.render_photos_button.setEnabled(False)
        self.ui.render_film_button.setEnabled(False)

    def connect_report_page_controller(self):
        self.ui.save_report.clicked.connect(self.generate_report_page_controller.export_report_pdf)

    def connect_add_trainee_page_buttons(self):
        self.map_button_event('add_trainee_button', [
            self.add_trainee_get_value,
            lambda: self.view_trainee_page_controller.set_values_on_trainees_page(self.trainee),
            self.view_trainee_page_controller.open_view_trainee_page
        ])
        self.ui.add_trainee_button.clicked.connect(lambda: self.handle_button_event('add_trainee_button'))

    def connect_view_training_page_buttons(self):
        self.ui.prev_training_button.clicked.connect(self.view_training_page_controller.show_prev_training)
        self.ui.next_training_button.clicked.connect(self.view_training_page_controller.show_next_training)

    def connect_report_page_buttons(self):
        self.ui.next_photo_button.clicked.connect(self.generate_report_page_controller.next_photo)
        self.ui.prev_photo_button.clicked.connect(self.generate_report_page_controller.prev_photo)

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
        self.view_trainee_page_controller.set_values_on_trainees_page(self.trainee)
        self.ui.stackedWidget.setCurrentWidget(self.ui.view_trainee_page)

    def open_add_training_name(self):
        self.list_of_trainees_controller.refresh_list_trainees(self.db_manager)
        self.add_training_name_controller.set_trainees_checkbox(self.table_of_trainees, self.trainee)

    def create_training(self):
        if self.add_training_name_controller.validate_data_add_training_name():
            return

        self.trainee = self.add_training_page_controller.select_trainee_info_combobox(self.table_of_trainees)
        self.list_of_exercises = []
        self.workout = self.add_training_page_controller.create_workout(self.trainee.id)
        self.add_training_page_controller.open_add_training_page()

    def add_exercises(self):
        self.list_of_exercises = self.add_training_page_controller.add_exercise()

    def add_training(self):
        if not self.add_training_page_controller.add_training(self.db_manager, self.workout):
            return
        self.view_training_page_controller.open_view_training_page(self.trainee, self.workout)

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
