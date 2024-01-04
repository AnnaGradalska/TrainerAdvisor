from PyQt5.QtWidgets import QTableWidgetItem

from src.core.database_handlers.customized_exercises import CustomizedExercises
from src.core.database_handlers.workouts import Workouts


class ViewTrainingPageController:
    def __init__(self, ui, db_manager):
        self.ui = ui
        self.current_training_index = 0
        self.db_manager = db_manager

    def open_view_training_page(self, trainee):
        self.ui.training_table.setRowCount(0)
        workouts = trainee.select_all_trainings(self)
        if not workouts:
            return
        workouts = [i[0] for i in workouts]
        exercises = CustomizedExercises.get_customized_exercises_for_trainee(workouts, self.db_manager)
        if not exercises:
            return

        # Grupowanie ćwiczeń według numeru treningu
        self.grouped_exercises = {}
        for exercise in exercises:
            training_number = exercise[2]
            if training_number not in self.grouped_exercises:
                self.grouped_exercises[training_number] = []
            self.grouped_exercises[training_number].append(exercise)


        self.training_indexes = list(self.grouped_exercises.keys())

        if self.grouped_exercises:
            self.current_training_index = self.training_indexes[0]
        else:
            self.current_training_index = None

        result = self.update_current_training_values()
        if not result:
            return False

        self.ui.stackedWidget.setCurrentWidget(self.ui.view_training_page)
        return result

    def update_current_training_values(self):
        self.ui.training_table.setRowCount(0)

        for exercise in self.grouped_exercises.get(self.current_training_index, []):
            row_position = self.ui.training_table.rowCount()
            self.ui.training_table.insertRow(row_position)

            selected_values = [exercise[i] for i in [1, 3, 4, 5]]

            # Wstawianie danych do tabeli
            for column, value in enumerate(selected_values):
                item = QTableWidgetItem(str(value))
                self.ui.training_table.setItem(row_position, column, item)


        workout_data = Workouts.get_workout_from_db_by_id(
            self.db_manager, self.current_training_index)
        if not workout_data:
            return False
        elif workout_data:
            self.ui.title_training.setText(workout_data[0][2])
            return True
        else:
            self.ui.title_training.setText("")
            return True

    def show_next_training(self):
        if self.training_indexes:
            current_training_index = self.training_indexes.index(self.current_training_index)
            next_index = (current_training_index + 1) % len(self.training_indexes)
            self.current_training_index = self.training_indexes[next_index]
            result = self.update_current_training_values()
            if not result:
                return False

            return True

    def show_prev_training(self):
        if self.training_indexes:
            current_training_index = self.training_indexes.index(self.current_training_index)
            prev_index = (current_training_index - 1) % len(self.training_indexes)
            self.current_training_index = self.training_indexes[prev_index]
            result = self.update_current_training_values()
            if not result:
                return False

            return True
