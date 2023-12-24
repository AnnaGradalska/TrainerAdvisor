from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox

from src.core.add_training_name_controller import AddTrainingNameController
from src.core.add_training_page_controller import AddTrainingPageController
from src.core.customized_exercises import CustomizedExercises
from src.core.generate_report_page_controller import GenerateReportPageController
from src.core.trainees import Trainees
from src.core.view_training_page_controller import ViewTrainingPageController
from src.core.workouts import Workouts
from src.data.database_manager import DatabaseManager
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from menu_page_controller import MenuPageController
from navbar_controller import NavbarController
from list_of_trainees_controller import ListOfTraineesController
from add_trainee_page_controller import AddTraineePageController
from view_trainee_page_controller import ViewTraineePageController




class ButtonController:

    def __init__(self, ui, main_win):

        # self.model = QStandardItemModel()
        self.ui = ui
        self.main_win = main_win
        self.button_event_mappings = {}
        self.db_manager = DatabaseManager()
        # navbar_controller
        self.navbar_controller = NavbarController(self.ui)
        # mainPage
        self.menu_page_controller = MenuPageController(self.ui)
        self.list_of_trainees_controller = ListOfTraineesController(self.ui)
        self.add_trainee_page_controller = AddTraineePageController(self.ui)
        self.view_trainee_page_controller = ViewTraineePageController(self.ui)
        self.add_training_name_controller = AddTrainingNameController(self.ui)
        self.add_training_page_controller = AddTrainingPageController(self.ui)
        self.view_training_page_controller = ViewTrainingPageController(self.ui, self.db_manager)
        self.generate_report_page_controller = GenerateReportPageController(self.main_win)
        self.connect_buttons()


        self.trainee = Trainees('name', 'surname', 'email', '2000-01-01', 999999999, 'training_start_date', 99, 99, 99,
                                99)
        self.workout = Workouts(0, 'workout', '2000-01-01')
        self.table_of_trainees = self.list_of_trainees_controller.refresh_list_trainees(self.db_manager)
        self.num = 99
        self.list_of_exercises = []
        self.model_exercises = QStandardItemModel()

        print(self.trainee.select_all(self.db_manager))

        #self.refresh_list_trainees()

    # wzorzec obserwatora do zarządzania tymi zdarzeniami
    def map_button_event(self, button, event_handler):
        self.button_event_mappings[button] = event_handler
        print(self.button_event_mappings)

    def handle_button_event(self, button):
        try:
            for event_handler in self.button_event_mappings[button]:
                event_handler()
        except Exception as e:
            print(f"Error during handle_button_event: {e}")

    def add_trainee_get_value(self):
        self.trainee = self.add_trainee_page_controller.add_trainee(self.db_manager)


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
        # menu_buttons
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
            lambda: self.view_trainee_page_controller.delete_trainee(self.db_manager))

    def connect_add_training_name_buttons(self):
        self.ui.move_to_add_exercises_button.clicked.connect(self.create_training)

    def connect_add_training_page_buttons(self):
        self.ui.add_next_excercise_button.clicked.connect(self.add_exercises)
        self.ui.add_training_button.clicked.connect(self.add_training)

    def connect_generate_report_page_buttons(self):
        self.ui.add_photos_button.clicked.connect(self.generate_report_page_controller.choose_picture)

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
        # dodać opcje w przypadku zmienienia w combobox podopiecznego
        if(self.add_training_name_controller.validate_data_add_training_name()):
            return

        self.trainee = self.add_training_page_controller.select_trainee_info_combobox(self.table_of_trainees)
        self.list_of_exercises = []
        self.workout = self.add_training_page_controller.create_workout(self.trainee.id)
        self.add_training_page_controller.open_add_training_page()


    # pamiętaj o wyzerowaniu listy przy dodawaniu treningu
    def add_exercises(self):
        self.list_of_exercises = self.add_training_page_controller.add_exercise()

    def add_training(self):
        self.add_training_page_controller.add_training(self.db_manager, self.workout)
        self.view_training_page_controller.open_view_training_page(self.trainee, self.workout)



    # def delete_trainee(self):
    #     self.trainee.delete_trainee_from_db(self.db_manager)
    #     print("usunięto")
    #     self.list_of_trainees_controller.refresh_list_trainees(self.db_manager)
    #     self.menu_page_controller.open_page(self.ui.main_page)

    # @staticmethod
    # def show_popup(message):
    #     msg = QMessageBox()
    #     msg.setIcon(QMessageBox.Warning)
    #     msg.setText(message)
    #     msg.setWindowTitle("Warning")
    #     msg.exec_()
