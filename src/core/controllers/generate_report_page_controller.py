import os

import cv2
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from src.core.image_processing_tools.image_processing import process_image
from src.core.controllers.report_page_controller import ReportPageController
from src.core.reporting_pdf.report_pdf import ReportPDF
from src.core.image_processing_tools.technical_squat_analysis import analyze_squat_inclination, analyze_knees_position, analyze_squat_depth


class GenerateReportPageController:
    def __init__(self, main_win, ui):
        self.main_win = main_win
        self.ui = ui
        self.paths_to_photos = ""
        self.report_page_controller = None
        self.path_to_film = ""
        self.paths_to_photos = []
        self.dir = ""
        self.report_photos_paths = []
        self.all_photos_skeleton_points = []

    def open_film(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_to_film, _ = QFileDialog.getOpenFileName(self.main_win, "Open File", "C:\\",
                                                           "Films (*.mp4);;All Files (*)", options=options)

        if not self.path_to_film:
            self.show_popup("Nie wybrano pliku")
            return

        self.ui.render_film_button.setEnabled(True)

    def open_photos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Określenie dopuszczalnych rozszerzeń plików
        file_filter = "Photos (*.png *.jpg);;All Files (*)"

        # Ograniczenie do maksymalnie 5 plików
        self.paths_to_photos, _ = QFileDialog.getOpenFileNames(self.main_win, "Open Files", "C:\\", file_filter, options=options)

        # Ograniczenie do maksymalnie 5 ścieżek
        if len(self.paths_to_photos) != 5:
            GenerateReportPageController.show_popup("Nie wybrano 5 zdjęć!")
            return

        self.ui.render_photos_button.setEnabled(True)

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
            self.show_popup(f"Wystąpił błąd: {e}")
            return
        finally:
            # Zamknij plik wideo
            cap.release()

        if not self.render_photos(images_paths):
            return

        description = self.analyze_squat_technique()
        self.ui.report_comment.setPlainText(description)
        self.ui.stackedWidget.setCurrentWidget(self.ui.report_page)

    def generate_report_photos(self):
        file_name, _ = os.path.splitext(os.path.basename(self.paths_to_photos[0]))
        self.dir = f"report_photos/{file_name}"

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not self.render_photos(self.paths_to_photos):
            return

        description = self.analyze_squat_technique()
        self.ui.report_comment.setPlainText(description)
        self.ui.stackedWidget.setCurrentWidget(self.ui.report_page)

    def render_photos(self, images_paths):
        self.report_photos_paths, self.all_photos_skeleton_points = process_image(images_paths, self.dir)

        if not self.report_photos_paths:
            return False

        self.report_page_controller = ReportPageController(self.ui, self.report_photos_paths)

        return True

    def next_photo(self):
        self.report_page_controller.next_photo()

    def prev_photo(self):
        self.report_page_controller.prev_photo()

    def get_save_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Wyłączamy natywne okno dialogowe systemu
        # Wyświetlamy okno dialogowe
        save_path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", "", "All Files (*)", options=options)
        return save_path

    def export_report_pdf(self):
        try:
            pdf = ReportPDF()
            pdf.set_page_layout()
            pdf.add_images(self.report_photos_paths)
            pdf.add_report_header("Raport")
            pdf.add_description("Opis", 100)
            print(self.ui.report_comment.toPlainText())
            pdf.add_text(self.ui.report_comment.toPlainText())
            pdf.generate_pdf("Raport")
        except Exception as e:
            self.show_popup(f"Error: {e}")

    def analyze_squat_technique(self):
        analysis_description = "--- Wygenerowany raport - początek ---\n\n"
        analysis_description += analyze_squat_inclination(self.all_photos_skeleton_points)
        analysis_description += analyze_knees_position(self.all_photos_skeleton_points)
        analysis_description += analyze_squat_depth(self.all_photos_skeleton_points)
        analysis_description += "\n\n--- Wygenerowany raport - koniec ---\n\n"
        return analysis_description

    @staticmethod
    def show_popup(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
