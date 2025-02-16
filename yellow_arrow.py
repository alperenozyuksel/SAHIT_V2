from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPolygonF
from PyQt5.QtCore import QPointF, Qt

class YellowArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0  # Initial angle of the arrow (in degrees)

    def set_angle(self, angle):
        self.angle = angle
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the color to yellow
        painter.setBrush(QColor("yellow"))
        painter.setPen(Qt.NoPen)

        # Define the size of the arrow
        arrow_size = min(self.width(), self.height()) * 0.4
        center = QPointF(self.width() / 2, self.height() / 2)

        # Define the points of the arrow (triangle)
        arrow_points = [
            QPointF(center.x(), center.y() - arrow_size / 2),
            QPointF(center.x() - arrow_size / 4, center.y() + arrow_size / 4),
            QPointF(center.x() + arrow_size / 4, center.y() + arrow_size / 4)
        ]

        # Rotate the arrow based on the angle
        painter.translate(center)
        painter.rotate(self.angle)
        painter.translate(-center)

        # Draw the arrow
        painter.drawPolygon(QPolygonF(arrow_points))