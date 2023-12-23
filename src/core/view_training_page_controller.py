from PyQt5.QtWidgets import QTableWidgetItem

from src.core.customized_exercises import CustomizedExercises


class ViewTrainingPageController:
    def __init__(self, ui):
        self.ui = ui

    def open_view_training_page(self, trainee, workout, db_manager):
        print('przechodząc na training page')
        workouts = trainee.select_all_trainings(self)
        workouts = [i[0] for i in workouts]
        print(workouts)
        customized_exe = CustomizedExercises("none", "none", "none", "none", "none")
        exercises = CustomizedExercises.get_customized_exercises_for_trainee(workouts)
        print(exercises)
        print(workout.select_all(db_manager))

        # Grupowanie ćwiczeń według numeru treningu
        grouped_exercises = {}
        for exercise in exercises:
            training_number = exercise[2]
            if training_number not in grouped_exercises:
                grouped_exercises[training_number] = []
            grouped_exercises[training_number].append(exercise)
        print(grouped_exercises)
        # Dodawanie danych do tabeli

        self.ui.stackedWidget.setCurrentWidget(self.ui.view_training_page)