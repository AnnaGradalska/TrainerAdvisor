from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.addWidget(self.canvas)
        self.setFixedSize(700, 500)

    def setup_plot(self, data):
        try:
            if not data:
                # Brak danych, nie rysujemy wykresu
                return

            # Rozdzielanie danych na trzy listy: daty, przysiad i martwy ciąg
            dates = [datetime.strptime(row[5], '%Y-%m-%d') for row in data]
            squat = [row[2] for row in data]
            deadlift = [row[4] for row in data]
            bench_press = [row[3] for row in data]

            self.canvas.figure.clear()
            self.canvas.figure.set_size_inches(6, 4)
            axes = self.canvas.figure.add_subplot(111)
            self.canvas.figure.patch.set_facecolor((0, 0, 0, 0))

            # Wykres przysiadu
            axes.plot(dates, squat, label='Przysiad', linestyle='--', color='#DB79B1', marker='o')

            # Wykres martwego ciągu
            axes.plot(dates, deadlift, label='Martwy ciąg', linestyle='--', color='#8577B5', marker='o')

            # Wykres wyciskania leżąc
            axes.plot(dates, bench_press, label='Wyciskanie leżąc',linestyle='--', color='#1F91C9', marker='o')

            axes.legend(loc='upper right')
            axes.set_title('Wykres personalnych rekordów', pad=20)
            axes.set_facecolor('#363435')
            axes.spines['bottom'].set_color('white')
            axes.spines['left'].set_color('white')
            axes.spines['top'].set_color('white')
            axes.spines['right'].set_color('white')
            axes.tick_params(axis='x', colors='white')
            axes.tick_params(axis='y', colors='white')
            axes.grid(True, linestyle='--', linewidth=0.5, color='#878285')
            axes.xaxis.label.set_color('white')
            axes.yaxis.label.set_color('white')
            axes.title.set_color('white')


            # Ustawienia osi x
            min_date, max_date = min(dates), max(dates)
            # Ustawienia osi x
            axes.set_xlim(min_date - timedelta(days=1), max_date + timedelta(days=60))
            axes.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=6))
            axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

            # Ustawienia osi y
            axes.set_ylim(0, 400)

            # Ustawienia osi
            axes.set_xlabel('Data')
            axes.set_ylabel('Ciężar [kg]', labelpad=10)

            plt.xticks(rotation=45, ha='right', rotation_mode='anchor')  # Obróć etykiety osi x dla lepszej czytelności

            self.canvas.draw()
            self.setLayout(self.vertical_layout)
            self.canvas.figure.tight_layout()

        except Exception as e:
            print(e)
