from operator import itemgetter

from PyQt5 import QtCore
from src.core.controllers.plot_widget import MplWidget




class PlotPersonalRecordsPageController:
    def __init__(self, ui, db_manager):
        self.ui = ui
        self.db_manager = db_manager
        self.plot_widget = MplWidget(self.ui.plot_personal_records_page)
        self.plot_widget.setGeometry(QtCore.QRect(100, 150, 671, 381))
        self.plot_widget.setObjectName("plot_widget")

    def setup_plot(self, data):
        self.plot_widget.setup_plot(data)

    def open_plot_personal_records_page(self, trainee):
        personal_records = trainee.select_all_personal_records(self.db_manager)
        if not personal_records:
            return

        personal_records.sort(key=itemgetter(5))
        self.setup_plot(personal_records)


        self.ui.stackedWidget.setCurrentWidget(self.ui.plot_personal_records_page)
        #return result






