from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import *

from vista.grafo.GraphNodeItem import GraphNodeItem
from vista.grafo.NodeData import NodeData
from vista.ventanaStats.ContactDetailDialog import ContactDetailDialog
from vista.pantallas.InteractiveView import InteractiveView

class MainGameUI (QWidget):
    def __init__(self, switch_to_defeat):
        super().__init__()
        self.suspicion_label = None
        self.suspicion_bar = None
        self.influence_label = None
        self.money_label = None
        self.capital_label = None
        self.player_name_label = None
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
        self.network_view = InteractiveView(self.scene)
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
