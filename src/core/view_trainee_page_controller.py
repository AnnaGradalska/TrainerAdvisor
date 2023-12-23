class ViewTraineePageController:
    def __init__(self, ui):
        self.ui = ui

    def open_view_trainee_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.view_trainee_page)

    def set_values_on_trainees_page(self, trainee):
        self.ui.name_surname_dblabel.setText(trainee.name + " " + trainee.surname)
        self.ui.date_of_birth_label_dblabel.setText(trainee.date_of_birth)
        self.ui.email_dblabel.setText(trainee.email)
        self.ui.phone_dblabel.setText(trainee.phone)
        self.ui.weight_dblabel.setText(str(trainee.weight))
        self.ui.start_date_training_db_label.setText(str(trainee.training_start_date))
        self.ui.squat_dblabel.setText(str(trainee.squat))
        self.ui.benchpress_dblabel.setText(str(trainee.benchpress))
        self.ui.deadlift_dblabel.setText(str(trainee.deadlift))

    def delete_trainee(self, db_manager):
        self.trainee.delete_trainee_from_db(self.db_manager)
        print("usunięto")
        self.list_of_trainees_controller.refresh_list_trainees(self.db_manager)
        self.menu_page_controller.open_page(self.ui.main_page)