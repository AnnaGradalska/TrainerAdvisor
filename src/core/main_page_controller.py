class MainPageController:
    def __init__(self, ui):
        self.ui = ui

    def open_list_of_trainees_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.list_of_trainees_page)