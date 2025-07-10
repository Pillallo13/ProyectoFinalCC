from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, QPointF
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QWheelEvent, QMouseEvent

from modelo.entidades.NodeData import NodeData
from vista.grafo.GraphNodeItem import GraphNodeItem
from vista.ventana.ContactDetailDialog import ContactDetailDialog
from vista.pantallas.elementosGlobales.InteractiveView import InteractiveView
from controlador.red_politica.NodoController import NodoController


class MainGameHistoriaUI(QWidget):
    """
    Vista principal del juego.
    """

    def __init__(self, switch_to_defeat):
        super().__init__()
        self.setObjectName("MainGameHistoriaUI")

        self.switch_to_defeat = switch_to_defeat
        self.controller = NodoController()

        self.player_name_label = None
        self.capital_label = None
        self.money_label = None
        self.influence_label = None
        self.suspicion_label = None
        self.suspicion_bar = None

        main_layout = QVBoxLayout(self)

        graphics_container = QFrame(self)
        graphics_layout = QVBoxLayout(graphics_container)
        graphics_layout.setContentsMargins(0, 0, 0, 0)
        graphics_layout.setSpacing(0)

        self.scene = QGraphicsScene()
        self.network_view = InteractiveView(self.scene)
        self.network_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.overlay_hud = self.create_overlay_hud()
        self.overlay_hud.setParent(self.network_view.viewport())
        self.overlay_hud.move(10, 10)

        # Conectar señal para que el HUD se mueva con la vista
        self.network_view.view_changed.connect(self.update_hud_position)

        graphics_layout.addWidget(self.network_view)
        main_layout.addWidget(graphics_container, 1)

        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()
        self.btn_end_turn = QPushButton("FINALIZAR TURNO")
        self.btn_end_turn.setObjectName("GoldenButton")
        bottom_bar.addWidget(self.btn_end_turn)
        main_layout.addLayout(bottom_bar)

        self.populate_network_example()

    def create_overlay_hud(self) -> QFrame:
        hud_widget = QFrame()
        hud_widget.setObjectName("MiniHUD")
        hud_layout = QVBoxLayout(hud_widget)
        hud_layout.setContentsMargins(12, 12, 12, 12)
        hud_layout.setSpacing(8)

        self.player_name_label = QLabel("Nombre Jugador: El Gran Maquiavelo de los Llanos")
        self.player_name_label.setStyleSheet("font-weight: bold; color: white;")
        self.capital_label = QLabel("Capital Político: 1,000,000")
        self.money_label = QLabel("Dinero Sucio: $500,000")
        self.influence_label = QLabel("Influencia: 250")
        self.suspicion_label = QLabel("Sospecha:")
        self.suspicion_bar = QProgressBar()
        self.suspicion_bar.setValue(10)
        self.suspicion_bar.setFixedWidth(180)

        for widget in [
            self.player_name_label, self.capital_label, self.money_label,
            self.influence_label, self.suspicion_label, self.suspicion_bar
        ]:
            hud_layout.addWidget(widget)

        hud_widget.setStyleSheet("""
            QFrame#MiniHUD {
                background-color: rgba(0, 0, 0, 160);
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
        """)

        hud_widget.setFixedSize(240, 190)
        return hud_widget

    def update_hud_position(self):
        """
        Reposiciona el HUD para que siempre esté visible en la parte superior izquierda
        de la vista, incluso cuando se hace scroll o pan.
        """
        self.overlay_hud.move(10, 10)

    def populate_network_example(self):
        node1_data = self.controller.buscar_por_id(1)
        node2_data = self.controller.buscar_por_id(2)
        node3_data = self.controller.buscar_por_id(3)

        node1_item = GraphNodeItem(node1_data)
        node2_item = GraphNodeItem(node2_data)
        node3_item = GraphNodeItem(node3_data)

        node1_item.setPos(0, -150)
        node2_item.setPos(-150, 0)
        node3_item.setPos(150, 0)

        node1_item.node_clicked.connect(self.show_contact_details)
        node2_item.node_clicked.connect(self.show_contact_details)
        node3_item.node_clicked.connect(self.show_contact_details)

        self.scene.addItem(node1_item)
        self.scene.addItem(node2_item)
        self.scene.addItem(node3_item)

        pen = QPen(QColor("#555"), 2, Qt.PenStyle.SolidLine)
        self.scene.addLine(QLineF(node1_item.pos(), node2_item.pos()), pen)
        self.scene.addLine(QLineF(node1_item.pos(), node3_item.pos()), pen)

    def show_contact_details(self, node_data: NodeData):
        dialog = ContactDetailDialog(node_data, self)
        dialog.exec()

    def update_player_name(self, name: str):
        self.player_name_label.setText(f"Nombre Jugador: {name}")


class InteractiveView(QGraphicsView):
    """
    Vista interactiva personalizada que permite hacer zoom y desplazarse
    con el mouse. Emite una señal cada vez que la vista cambia para actualizar elementos flotantes.
    """

    view_changed = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event: QWheelEvent):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)
        self.view_changed.emit()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        self.view_changed.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.view_changed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.view_changed.emit()

    def scrollContentsBy(self, dx: int, dy: int):
        super().scrollContentsBy(dx, dy)
        self.view_changed.emit()
