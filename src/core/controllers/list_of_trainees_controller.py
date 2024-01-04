from PyQt5.QtGui import QStandardItem, QStandardItemModel
from trainees import Trainees


class ListOfTraineesController:
    def __init__(self, ui):
        self.ui = ui
        self.model = QStandardItemModel()
        self.table_of_trainees = []
        self.trainee = Trainees('name', 'surname', 'email', '2000-01-01', 999999999, 'training_start_date', 99, 99, 99,
                                99)

    def open_page(self, page):
        self.ui.stackedWidget.setCurrentWidget(page)

    def refresh_list_trainees(self, db_manager):
        self.model.removeRows(0, self.model.rowCount())
        result = self.trainee.select_all(db_manager)

        if not result:
            return False
        self.table_of_trainees = result

        for record in self.table_of_trainees:
            item = QStandardItem(" ".join((record[1], record[2])))
            self.model.appendRow(item)

        self.ui.list_of_trainees.setModel(self.model)

        return self.table_of_trainees
