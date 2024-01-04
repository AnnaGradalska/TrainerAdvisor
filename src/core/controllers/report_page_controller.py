from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ReportPageController:
    def __init__(self, ui, report_images_paths):
        self.ui = ui
        self.report_images_paths = report_images_paths
        self.index_of_current_picture = 0
        self.set_image()

    def next_photo(self):
        print("w funkcji")
        self.index_of_current_picture = self.index_of_current_picture + 1
        if self.index_of_current_picture >= len(self.report_images_paths):
            self.index_of_current_picture = 0

        self.set_image()



    def prev_photo(self):
        self.index_of_current_picture = self.index_of_current_picture - 1
        if self.index_of_current_picture <= 0:
            self.index_of_current_picture = len(self.report_images_paths) - 1

        self.set_image()

    def set_image(self):
        image_path = self.report_images_paths[self.index_of_current_picture]
        print('setimg')
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.ui.report_photo.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        print(pixmap)

        # Ustaw obraz w QLabel
        self.ui.report_photo.setPixmap(pixmap)
        print('setimg3')


