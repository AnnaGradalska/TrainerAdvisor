from PyQt5.QtWidgets import QMessageBox, QFileDialog


class GenerateReportPageController:
    def __init__(self, main_win):
        self.main_win = main_win

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

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()