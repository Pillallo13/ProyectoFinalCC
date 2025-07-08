from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import *

from modelo.entidades.NodeData import NodeData
from vista.grafo.GraphNodeItem import GraphNodeItem
from vista.ventana.ContactDetailDialog import ContactDetailDialog
from vista.pantallas.elementosGlobales.InteractiveView import InteractiveView
from controlador.red_politica.NodoController import NodoController


class MainGameHistoriaUI(QWidget):
    """
    Vista principal del juego.

    Esta clase representa la interfaz principal durante una partida.
    Contiene el área del grafo con los personajes corruptos, un HUD con estadísticas
    del jugador y un botón para finalizar turno.

    Se encarga de renderizar los nodos y sus conexiones, así como permitir al
    jugador consultar los detalles de cada contacto corrupto.

    Atributos:
        switch_to_defeat (callable): Función para cambiar a la pantalla de derrota.
        controller (NodoController): Controlador que gestiona el acceso a los datos de nodos.
        player_name_label (QLabel): Etiqueta que muestra el nombre del jugador.
        capital_label (QLabel): Muestra el capital político actual.
        money_label (QLabel): Muestra el dinero sucio disponible.
        influence_label (QLabel): Muestra los puntos de influencia.
        suspicion_bar (QProgressBar): Barra de nivel de sospecha.
    """

    def __init__(self, switch_to_defeat):
        """
        Inicializa la interfaz principal del juego.

        Args:
            switch_to_defeat (callable): Función que cambia la vista a la pantalla de derrota.
        """
        super().__init__()
        self.setObjectName("MainGameHistoriaUI")

        self.switch_to_defeat = switch_to_defeat
        self.controller = NodoController()

        # Inicialización explícita de referencias
        self.player_name_label = None
        self.capital_label = None
        self.money_label = None
        self.influence_label = None
        self.suspicion_label = None
        self.suspicion_bar = None

        # Layout general
        main_layout = QVBoxLayout(self)

        # Contenedor del grafo
        graphics_container = QFrame(self)
        graphics_layout = QVBoxLayout(graphics_container)
        graphics_layout.setContentsMargins(0, 0, 0, 0)
        graphics_layout.setSpacing(0)

        # Vista del grafo
        self.scene = QGraphicsScene()
        self.network_view = InteractiveView(self.scene)
        self.network_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # HUD flotante sobre la vista del grafo
        self.overlay_hud = self.create_overlay_hud()
        self.overlay_hud.setParent(self.network_view.viewport())
        self.overlay_hud.move(10, 10)

        graphics_layout.addWidget(self.network_view)
        main_layout.addWidget(graphics_container, 1)

        # Barra inferior con el botón de finalizar turno
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()
        self.btn_end_turn = QPushButton("FINALIZAR TURNO")
        self.btn_end_turn.setObjectName("GoldenButton")
        bottom_bar.addWidget(self.btn_end_turn)
        main_layout.addLayout(bottom_bar)

        # Renderizar nodos iniciales
        self.populate_network_example()

    def create_overlay_hud(self) -> QFrame:
        """
        Crea el HUD flotante que muestra los datos del jugador.

        Returns:
            QFrame: Widget con estadísticas superpuestas al grafo.
        """
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
        """
        Agrega los nodos de ejemplo a la escena del grafo.

        Obtiene los datos desde el controlador y los convierte en elementos visuales,
        incluyendo conexiones entre ellos.
        """
        node1_data = self.controller.buscar_por_id(1)
        node2_data = self.controller.buscar_por_id(2)
        node3_data = self.controller.buscar_por_id(3)

        node1_item = GraphNodeItem(node1_data)
        node2_item = GraphNodeItem(node2_data)
        node3_item = GraphNodeItem(node3_data)

        node1_item.setPos(0, -150)
        node2_item.setPos(-150, 0)
        node3_item.setPos(150, 0)

        # Conectar señales para mostrar detalles
        node1_item.node_clicked.connect(self.show_contact_details)
        node2_item.node_clicked.connect(self.show_contact_details)
        node3_item.node_clicked.connect(self.show_contact_details)

        # Añadir nodos y conexiones al grafo
        self.scene.addItem(node1_item)
        self.scene.addItem(node2_item)
        self.scene.addItem(node3_item)

        pen = QPen(QColor("#555"), 2, Qt.PenStyle.SolidLine)
        self.scene.addLine(QLineF(node1_item.pos(), node2_item.pos()), pen)
        self.scene.addLine(QLineF(node1_item.pos(), node3_item.pos()), pen)

    def show_contact_details(self, node_data: NodeData):
        """
        Muestra el cuadro de diálogo con los detalles del contacto seleccionado.

        Args:
            node_data (NodeData): Nodo cuyos datos se mostrarán.
        """
        dialog = ContactDetailDialog(node_data, self)
        dialog.exec()

    def update_player_name(self, name: str):
        """
        Actualiza el nombre del jugador en el HUD.

        Args:
            name (str): Nuevo nombre del jugador.
        """
        self.player_name_label.setText(f"Nombre Jugador: {name}")
