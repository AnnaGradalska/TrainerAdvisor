import math
import os

import cv2
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from src.core.image_processing import process_image
from src.core.report_page_controller import ReportPageController


class GenerateReportPageController:
    def __init__(self, main_win, ui):
        self.main_win = main_win
        self.paths_to_photos = ""
        self.ui = ui
        self.report_page_controller = None
        self.path_to_film = ""
        self.paths_to_photos = []
        self.dir = ""

        # def choose_picture(self):

    #     options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     paths_to_photos, _ = QFileDialog.getOpenFileNames(self.main_win, "Open File", "C:\\",
    #                                                       "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
    #
    #     if len(paths_to_photos) != 5:
    #         self.show_popup("Wybierz dokładnie 5 zdjęć!")
    #         return
    #
    #     if paths_to_photos:
    #         for path in paths_to_photos:
    #             print(path)

    def open_film(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_to_film, _ = QFileDialog.getOpenFileName(self.main_win, "Open File", "C:\\",
                                                              "Films (*.mp4);;All Files (*)", options=options)

        if not self.path_to_film:
            print("Nie wybrano pliku")
            return

        print(f"Wybrano plik: {self.path_to_film}")

    def open_photos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Określenie dopuszczalnych rozszerzeń plików
        file_filter = "Photos (*.png *.jpg);;All Files (*)"

        # Ograniczenie do maksymalnie 5 plików
        self.paths_to_photos, _ = QFileDialog.getOpenFileNames(
            self.main_win, "Open Files", "C:\\", file_filter, options=options
        )

        if not self.paths_to_photos:
            print("Nie wybrano pliku")
            return

        # Ograniczenie do maksymalnie 5 ścieżek
        self.paths_to_photos = self.paths_to_photos[:5]

        print(f"Wybrano pliki: {self.paths_to_photos}")

    def generate_report_film(self):
        file_name, _ = os.path.splitext(os.path.basename(self.path_to_film))
        cap = cv2.VideoCapture(self.path_to_film)
        self.dir = f"report_photos/{file_name}"
        images_paths = []

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        # Sprawdź, czy plik wideo został poprawnie otwarty
        if not cap.isOpened():
            print("Błąd otwierania pliku wideo.")
            return

        try:
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Określ momenty, w których chcesz robić zrzuty (w sekundach)
            snapshot_times = [0, 2 * fps, 4 * fps, 8 * fps, 9 * fps]

            # Przejdź przez każdą klatkę
            for frame_number in snapshot_times:

                # Ustaw pozycję na konkretnej klatce
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

                # Odczytaj klatkę
                ret, frame = cap.read()

                # Sprawdź, czy odczyt klatki był udany
                if ret:
                    # Zapisz klatkę jako obraz
                    output_path = f"report_photos/{file_name}/frame_{frame_number}.png"
                    images_paths.append(output_path)
                    cv2.imwrite(output_path, frame)
                    print(f"Zapisano klatkę {frame_number} do {output_path}")
                else:
                    print(f"Błąd odczytu klatki w sekundzie {frame_number}")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            # Zamknij plik wideo
            cap.release()

        self.render_photos(images_paths)
        process_image(images_paths, self.dir)
        self.ui.stackedWidget.setCurrentWidget(self.ui.report_page)

    def generate_report_photos(self):
        #print(images_paths)
        file_name, _ = os.path.splitext(os.path.basename(self.paths_to_photos[0]))
        self.dir = f"report_photos/{file_name}"
        print(self.dir)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.render_photos(self.paths_to_photos)
        self.ui.stackedWidget.setCurrentWidget(self.ui.report_page)

    def render_photos(self, images_paths):
        print("w render_photos")
        print(images_paths)
        report_photos_paths = process_image(images_paths, self.dir)
        print("po")
        self.report_page_controller = ReportPageController(self.ui, report_photos_paths)

    def next_photo(self):
        self.report_page_controller.next_photo()

    def prev_photo(self):
        self.report_page_controller.prev_photo()

    #def export_report_pdf(self):


    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
