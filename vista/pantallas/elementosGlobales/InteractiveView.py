from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QPoint


class InteractiveView(QGraphicsView):
    """
    Vista gráfica interactiva personalizada que permite hacer zoom con la rueda del mouse
    y desplazamiento usando clic derecho.

    Esta clase extiende QGraphicsView para mejorar la experiencia de navegación
    sobre escenas complejas, como un grafo de nodos.
    """

    def __init__(self, scene, parent=None):
        """
        Inicializa la vista interactiva con una escena de gráficos.

        Args:
            scene (QGraphicsScene): Escena a visualizar.
            parent (QWidget, opcional): Widget padre, si lo hay.
        """
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._is_panning = False
        self._pan_start = QPoint()

    def wheelEvent(self, event):
        """
        Maneja el evento de la rueda del mouse para hacer zoom in o out.

        Args:
            event (QWheelEvent): Evento de rueda del mouse.
        """
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        """
        Inicia el modo de desplazamiento (pan) si se presiona clic derecho.

        Args:
            event (QMouseEvent): Evento de presión del mouse.
        """
        if event.button() == Qt.MouseButton.RightButton:
            self._is_panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Mueve la vista mientras se arrastra con clic derecho (pan activo).

        Args:
            event (QMouseEvent): Evento de movimiento del mouse.
        """
        if self._is_panning:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._pan_start)
            self._pan_start = event.pos()
            self.translate(-delta.x(), -delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Finaliza el modo de desplazamiento al soltar clic derecho.

        Args:
            event (QMouseEvent): Evento de liberación del mouse.
        """
        if event.button() == Qt.MouseButton.RightButton:
            self._is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)
