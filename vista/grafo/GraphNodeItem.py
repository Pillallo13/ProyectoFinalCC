from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from modelo.entidades.NodeData import NodeData
from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtGui import *

class GraphNodeItem(QGraphicsObject):
    """
    Representa un nodo interactivo en el grafo visual del juego.

    Este objeto hereda de QGraphicsObject y se utiliza dentro de una QGraphicsScene.
    Cada instancia representa visualmente un personaje de la red corrupta, con su estado
    actual (activo, sospechoso, etc.), y responde a eventos de clic para mostrar su expediente.

    Atributos:
        node_clicked (Signal): Señal personalizada que emite el objeto NodeData asociado
                               cuando el nodo es clicado.
    """

    node_clicked = pyqtSignal(NodeData)

    def __init__(self, node_data: NodeData):
        """
        Inicializa el nodo visual con los datos del personaje.

        Args:
            node_data (NodeData): Objeto con los datos del personaje representado.
        """
        super().__init__()
        self.node_data = node_data
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Click para ver expediente de {self.node_data.name}")

        # Diccionario de colores por estado
        self.status_colors = {
            'Activo': QColor("#4CAF50"),         # Verde
            'Bajo Sospecha': QColor("#FFC107"),  # Amarillo
            'Investigado': QColor("#F44336"),    # Rojo
            'Quemado': QColor("#616161")         # Gris
        }

    def boundingRect(self) -> QRectF:
        """
        Define los límites del área ocupada por el nodo (para colisiones, pintura, etc.).

        Returns:
            QRectF: Rectángulo delimitador centrado en (0, 0) de 80x80.
        """
        return QRectF(-40, -40, 80, 80)

    def paint(self, painter: QPainter, option, widget=None):
        """
        Dibuja visualmente el nodo dentro de la escena.

        Muestra un círculo con borde de color según el estado y el nombre centrado abajo.

        Args:
            painter (QPainter): Objeto de dibujo.
            option: Opciones de estilo de Qt (no se usa aquí).
            widget: Widget padre si aplica (normalmente None).
        """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Borde de color según estado
        pen_color = self.status_colors.get(self.node_data.status, QColor("white"))
        pen = QPen(pen_color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#2C2C2C")))  # Relleno gris oscuro
        painter.drawEllipse(-35, -35, 70, 70)

        # Texto del nombre
        font = QFont("Roboto", 7)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(
            self.boundingRect(),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
            self.node_data.name
        )

    def mousePressEvent(self, event):
        """
        Detecta cuando el nodo es clicado y emite la señal con los datos del nodo.

        Args:
            event (QGraphicsSceneMouseEvent): Evento del clic del mouse.
        """
        self.node_clicked.emit(self.node_data)
        super().mousePressEvent(event)
