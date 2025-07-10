from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import *

from controlador.campanna.PersonajeController import PersonajeController
from modelo.entidades.campanna.NodeData import NodeData
from vista.grafo.GraphNodeItem import GraphNodeItem
from vista.ventana.ContactDetailDialog import ContactDetailDialog
from vista.pantallas.elementosGlobales.InteractiveView import InteractiveView
from controlador.campanna.NodoController import NodoController
from controlador.campanna.BiografiaController import BiografiaController

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
        self.BiografiaController = BiografiaController()

        # Inicialización explícita de referencias
        self.player_name_label = None
        self.capital_label = None
        self.money_label = None
        self.influence_label = None
        self.suspicion_label = None
        self.suspicion_bar = None
        self.PersonajeController = None
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


        self.player_name_label = QLabel(PersonajeController.nombre_completo)
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
        Dibuja todos los nodos desde el controller, sin conexiones.
        Distribuye los nodos en el espacio, considerando un diámetro de 80 px
        y una distancia mínima de separación entre centros.
        """
        from math import hypot
        import random

        self.scene.clear()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.items_por_id = {}
        self.posiciones_ocupadas = []

        nodos = self.controller.obtener_todos()

        # Configuración visual
        diametro_nodo = 80
        separacion_extra = 10
        distancia_minima = diametro_nodo + separacion_extra  # 120 px entre centros
        ancho_area, alto_area = 1000, 1000
        padding = distancia_minima

        def es_posicion_valida(x, y):
            for px, py in self.posiciones_ocupadas:
                if hypot(x - px, y - py) < distancia_minima:
                    return False
            return True

        for nodo in nodos:
            for _ in range(100):  # intenta 100 veces una buena posición
                x = random.randint(-ancho_area // 2 + padding, ancho_area // 2 - padding)
                y = random.randint(-alto_area // 2 + padding, alto_area // 2 - padding)
                if es_posicion_valida(x, y):
                    self.posiciones_ocupadas.append((x, y))
                    break
            else:
                # si no encuentra una válida, lo pone en algún lugar aleatorio sin validar
                x, y = random.randint(-2000, 2000), random.randint(-2000, 2000)

            node_item = GraphNodeItem(nodo)
            node_item.setPos(x, y)
            node_item.node_clicked.connect(self.show_contact_details)
            self.scene.addItem(node_item)
            self.items_por_id[nodo.id] = node_item

        # === 2. Dibujar conexiones entre los nodos ===

        for nodo in nodos:
            origen_item = self.items_por_id.get(nodo.id)
            for conexion in nodo.connected_to:
                if isinstance(conexion, dict):
                    destino_id = conexion.get("target_id")
                    peso = conexion.get("peso", 0)
                    tipo = conexion.get("tipo", "positiva")
                else:
                    destino_id = conexion
                    peso = 0
                    tipo = "positiva"

                destino_item = self.items_por_id.get(destino_id)
                if origen_item and destino_item:
                    # Establecer el color basado en el valor de peso
                    color = QColor("#00aa00") if peso > 0 else QColor(
                        "#aa0000")  # Verde si es positivo, Rojo si es negativo

                    # Definir grosor de la línea basado en el valor absoluto del peso
                    pen = QPen(color, 2 + abs(peso) / 50, Qt.PenStyle.SolidLine)

                    # Línea principal
                    linea = QLineF(origen_item.pos(), destino_item.pos())
                    self.scene.addLine(linea, pen)

                    # Flecha
                    from PyQt6.QtCore import QPointF
                    from PyQt6.QtGui import QPolygonF, QBrush

                    # Coordenadas de inicio y fin
                    start = linea.p1()
                    end = linea.p2()

                    # Vector unitario de dirección
                    dx = end.x() - start.x()
                    dy = end.y() - start.y()
                    length = (dx ** 2 + dy ** 2) ** 0.5
                    if length == 0:
                        return

                    ux = dx / length
                    uy = dy / length
                    arrow_size = 10

                    # Puntos de la flecha
                    p1 = QPointF(end.x() - arrow_size * ux + arrow_size * uy / 2,
                                 end.y() - arrow_size * uy - arrow_size * ux / 2)
                    p2 = QPointF(end.x() - arrow_size * ux - arrow_size * uy / 2,
                                 end.y() - arrow_size * uy + arrow_size * ux / 2)

                    flecha = QPolygonF([end, p1, p2])
                    self.scene.addPolygon(flecha, pen, QBrush(color))

    def show_contact_details(self, node_data: NodeData):
        """
        Muestra el cuadro de diálogo con los detalles del contacto seleccionado.

        Args:
            node_data (NodeData): Nodo cuyos datos se mostrarán.
        """
        dialog = ContactDetailDialog(node_data, self)
        dialog.exec()

    def update_player_name(self):
        """
        Actualiza el nombre del jugador en el HUD con el nombre cargado desde el controlador.
        """
        # Obtener el nombre del jugador desde el controlador BiografiaController
        nombre_jugador = self.BiografiaController.obtener_nombre_jugador()

        # Actualizar el texto del label en el HUD con el nombre del jugador
        self.player_name_label.setText(f"{nombre_jugador}")

