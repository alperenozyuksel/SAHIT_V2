import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRect


class ScaleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scale_min = 0  # Minimum değer
        self.scale_max = 300  # Maksimum değer (300'e kadar)
        self.scale_step = 25  # Büyük çizgiler arası mesafe (her 25 birimde bir büyük çizgi)
        self.minor_step = 5  # Küçük çizgiler arası mesafe (her 5 birimde bir küçük çizgi)

    def paintEvent(self, event):
        """Çizim fonksiyonu"""
        painter = QPainter(self)
        self.draw_scale(painter)

    def draw_scale(self, painter):
        """Ölçeği çizen fonksiyon"""
        # Çizim ayarları
        pen = QPen(Qt.white, 2)  # Büyük çizgiler için kalınlık
        painter.setPen(pen)
        font = QFont("Arial", 10, QFont.Bold)  # Etiket fontu
        painter.setFont(font)

        # Geometri ayarları
        margin = 20  # Kenar boşluğu
        scale_width = 30  # Ölçek genişliği
        start_y = margin
        end_y = self.height() - margin
        x = self.width() - margin  # Ölçeğin X pozisyonu

        # Ana ölçek çizgisi
        painter.drawLine(x, start_y, x, end_y)

        # Büyük ve küçük çizgi mesafeleri
        total_steps = (self.scale_max - self.scale_min) // self.scale_step
        step_size = (end_y - start_y) / total_steps  # Büyük çizgiler arası mesafe

        minor_step_size = step_size / (self.scale_step / self.minor_step)  # Küçük çizgi mesafesi

        # Ölçek üzerindeki tüm çizgileri çizme
        for i in range(self.scale_min, self.scale_max + 1, self.scale_step):
            y = end_y - ((i - self.scale_min) / (self.scale_max - self.scale_min)) * (end_y - start_y)

            # Son 3 çizgiyi kırmızıya boya
            if i >= self.scale_max - 3 * self.scale_step:
                pen.setColor(Qt.red)
            else:
                pen.setColor(Qt.white)

            painter.setPen(pen)
            painter.drawLine(x, y, x - scale_width, y)  # Büyük çizgi

            # Küçük çizgileri ekle
            pen.setWidth(1)
            painter.setPen(pen)
            for j in range(1, int(self.scale_step / self.minor_step)):
                minor_y = y - j * minor_step_size
                if minor_y < start_y:
                    break
                painter.drawLine(x, minor_y, x - scale_width // 2, minor_y)  # Küçük çizgi

            pen.setWidth(2)  # Ana çizgileri kalınlaştır
            painter.setPen(pen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScaleWidget()
    window.resize(200, 400)
    window.show()
    sys.exit(app.exec_())