from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from vista.grafo.NodeData import NodeData
from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtGui import *


class GraphNodeItem(QGraphicsObject):
    node_clicked = pyqtSignal(NodeData)

    def __init__(self, node_data: NodeData):
        super().__init__()
        self.node_data = node_data
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Click para ver expediente de {self.node_data.name}")

        self.status_colors = {
            'Activo': QColor("#4CAF50"),
            'Bajo Sospecha': QColor("#FFC107"),
            'Investigado': QColor("#F44336"),
            'Quemado': QColor("#616161")
        }

    def boundingRect(self):
        return QRectF(-40, -40, 80, 80)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen_color = self.status_colors.get(self.node_data.status, QColor("white"))
        pen = QPen(pen_color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#2C2C2C")))
        painter.drawEllipse(-35, -35, 70, 70)

        font = QFont("Roboto", 7)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, self.node_data.name)

    def mousePressEvent(self, event):
        self.node_clicked.emit(self.node_data)
        super().mousePressEvent(event)