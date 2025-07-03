from dataclasses import dataclass, field
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from vista.nodo import NodeData
from vista.vista_arbol_nodo import GraphNodeItem, ContactDetailDialog


class VistaInteractiva(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._is_panning = False
        self._pan_start = QPointF()

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._is_panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._pan_start)
            self._pan_start = event.pos()
            self.translate(-delta.x(), -delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

# --- VISTA 3: PANTALLA PRINCIPAL DEL JUEGO ---
class MainGameUI(QWidget):
    def __init__(self, switch_to_defeat):
        super().__init__()
        self.setObjectName("MainGameUI")
        self.switch_to_defeat = switch_to_defeat

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Contenedor del grafo y HUD flotante
        graphics_container = QFrame()
        graphics_layout = QVBoxLayout(graphics_container)
        graphics_layout.setContentsMargins(0, 0, 0, 0)
        graphics_layout.setSpacing(0)

        # Crear QGraphicsView
        self.scene = QGraphicsScene()
        self.network_view = VistaInteractiva(self.scene)
        self.network_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Crear HUD flotante incrustado sobre el área de grafo
        self.overlay_hud = self.create_overlay_hud()
        self.overlay_hud.setParent(self.network_view.viewport())
        self.overlay_hud.move(10, 10)

        graphics_layout.addWidget(self.network_view)
        main_layout.addWidget(graphics_container, 1)

        # Barra inferior para botón de finalizar turno
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()

        self.btn_end_turn = QPushButton("FINALIZAR TURNO")
        self.btn_end_turn.setObjectName("GoldenButton")
        bottom_bar.addWidget(self.btn_end_turn)

        main_layout.addLayout(bottom_bar)

        self.populate_network_example()

    def create_overlay_hud(self):
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

    def populate_network_example(self):
        node1_data = NodeData(1, "Alcalde Mermelada", "Alcalde", "Activo", 80, 50, 10, 50000, 5, 10000, "Contratación Amañada")
        node2_data = NodeData(2, "Concejal Tuerquilla", "Concejal", "Bajo Sospecha", 60, 75, 40, 20000, 2, 5000, "Compra de Votos")
        node3_data = NodeData(3, "Juez Prevaricatore", "Juez", "Investigado", 30, 90, 85, 150000, 10, 0, "Bloquear Investigación")

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

    def update_player_name(self, name):
        self.player_name_label.setText(f"Nombre Jugador: {name}")

# --- VISTA 4: PANTALLA DE DERROTA ---
class DefeatScreen(QWidget):
    def __init__(self, switch_to_main_menu):
        super().__init__()
        self.setObjectName("DefeatScreen")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("CAÍDA EN DESGRACIA")
        title.setStyleSheet("color: #D32F2F; font-size: 48px; font-weight: bold; font-family: 'Roboto Condensed';")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reason_label = QLabel("Causa: El Nivel de Sospecha ha alcanzado el 100%. La Fiscalía ha emitido una orden de captura.")
        self.reason_label.setWordWrap(True)
        self.reason_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_to_menu_button = QPushButton("VOLVER AL MENÚ PRINCIPAL")
        back_to_menu_button.clicked.connect(switch_to_main_menu)

        layout.addWidget(title)
        layout.addWidget(self.reason_label)
        layout.addSpacing(30)
        layout.addWidget(back_to_menu_button, alignment=Qt.AlignmentFlag.AlignCenter)
