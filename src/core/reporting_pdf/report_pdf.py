from PyQt5.QtWidgets import QFileDialog
from fpdf import FPDF


class ReportPDF(FPDF):
    def __init__(self, unit='mm', format='A4'):
        super().__init__(orientation='L', unit=unit, format=format)
        self.add_font('DejaVuBold', '', 'src/gui/resources/DejaVuSansCondensed-Bold.ttf', uni=True)
        self.add_font('DejaVu', '', 'src/gui/resources/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', size=12)

    def set_page_layout(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()

    def add_images(self, image_paths, image_width=48.4, image_height=86.1):
        x_start = self.get_x()
        y_start = self.get_y() + 30

        for image_path in image_paths:
            self.image(image_path, x_start, y_start, w=image_width, h=image_height)
            x_start += image_width

    def add_report_header(self):
        # self.add_font('DejaVu', '', 'src/gui/resources/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('')
        self.set_font('DejaVuBold', size=22)
        self.ln(10)
        self.cell(0, 10, "Raport", 0, 1, 'C')

    def add_description(self):
        #self.add_font('DejaVu', '', 'src/gui/resources/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('')
        self.set_font('DejaVuBold', size=14)
        self.ln(100)
        self.cell(0, 10, "Opis", 0, 1, 'L')

    def add_text(self, text):
        self.set_font('')
        self.set_font('DejaVu', size=12)
        self.multi_cell(0, 10, text)

    def generate_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Wyłączamy natywne okno dialogowe systemu
        # Wyświetlamy okno dialogowe
        save_path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", "Report.pdf", "PDF files (*.pdf);;All Files (*)", options=options)
        self.output(save_path)


