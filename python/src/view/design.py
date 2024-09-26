from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt

class CircleIcon(QWidget):
    def __init__(self, color=QColor("#FF0000"), size=10):
        super().__init__()
        self.color = color
        self.size = size
        self.setFixedSize(size + 4, size + 4)  # Set widget fixed size // +4 for padding

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Smooth edges
        brush = QBrush(self.color) # Set the fill color
        painter.setBrush(brush)  

        pen = QPen(Qt.NoPen)  # Remove Outline
        painter.setPen(pen)

        painter.drawEllipse(2, 2, self.size, self.size)  # Draw the circle
