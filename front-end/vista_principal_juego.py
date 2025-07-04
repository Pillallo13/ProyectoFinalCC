from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel,
                             QFrame, QProgressBar,
                             QGraphicsView, QGraphicsScene)
from PyQt6.QtGui import (QPainter, QColor, QPen)
from PyQt6.QtCore import Qt, QLineF
from nodo import NodeData 
from vista_arbol_nodo import GraphNodeItem, ContactDetailDialog

# --- VISTA 3: PANTALLA PRINCIPAL DEL JUEGO ---
class MainGameUI(QWidget):
    def __init__(self, switch_to_defeat):
        super().__init__()
        self.setObjectName("MainGameUI")
        self.switch_to_defeat = switch_to_defeat # Guardar la función para cambiar a la pantalla de derrota
        
        # Layout principal que divide la pantalla
        main_layout = QHBoxLayout(self)
        
        # --- Panel Central (Visualización) ---
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        # HUD Superior
        hud_panel = self.create_hud()
        
        # Área de visualización del grafo/árbol
        self.scene = QGraphicsScene()
        self.network_view = QGraphicsView(self.scene)
        self.network_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.populate_network_example()
        
        # LÓGICA A IMPLEMENTAR:
        # Aquí es donde instanciarías tu widget personalizado para dibujar el grafo/árbol.
        # Podrías usar QGraphicsView y QGraphicsScene para un control total.
        
        center_layout.addWidget(hud_panel)
        center_layout.addWidget(self.network_view, 1) # El '1' hace que se expanda

        # --- Panel Lateral Derecho (Acciones) ---
        side_panel = self.create_side_panel()

        main_layout.addWidget(center_panel, 3) # Ocupa 3/4 del espacio
        main_layout.addWidget(side_panel, 1)   # Ocupa 1/4 del espacio

    def populate_network_example(self):
        # LÓGICA DE JUEGO A IMPLEMENTAR:
        # Aquí, en lugar de crear datos de ejemplo, accederías a tu árbol
        # y recorrerías los nodos para crear los GraphNodeItem.

        # Datos de ejemplo
        node1_data = NodeData(1, "Alcalde Mermelada", "Alcalde", "Activo", 80, 50, 10, 50000, 5, 10000, "Contratación Amañada")
        node2_data = NodeData(2, "Concejal Tuerquilla", "Concejal", "Bajo Sospecha", 60, 75, 40, 20000, 2, 5000, "Compra de Votos")
        node3_data = NodeData(3, "Juez Prevaricatore", "Juez", "Investigado", 30, 90, 85, 150000, 10, 0, "Bloquear Investigación")

        # Crear items gráficos
        node1_item = GraphNodeItem(node1_data)
        node2_item = GraphNodeItem(node2_data)
        node3_item = GraphNodeItem(node3_data)

        # Posicionar items en la escena
        node1_item.setPos(0, -150)
        node2_item.setPos(-150, 0)
        node3_item.setPos(150, 0)

        # Conectar la señal de click de cada nodo a la función que muestra el diálogo
        node1_item.node_clicked.connect(self.show_contact_details)
        node2_item.node_clicked.connect(self.show_contact_details)
        node3_item.node_clicked.connect(self.show_contact_details)
        
        # Añadir items a la escena
        self.scene.addItem(node1_item)
        self.scene.addItem(node2_item)
        self.scene.addItem(node3_item)
        
        # --- SECCIÓN CORREGIDA ---
        # Dibujar líneas para mostrar jerarquía
        pen = QPen(QColor("#555"), 2, Qt.PenStyle.SolidLine)
        
        # Forma Correcta: Pasar el objeto QLineF directamente al método addLine
        line1 = QLineF(node1_item.pos(), node2_item.pos())
        self.scene.addLine(line1, pen)
        
        line2 = QLineF(node1_item.pos(), node3_item.pos())
        self.scene.addLine(line2, pen)
        

    def show_contact_details(self, node_data: NodeData):
        """Este slot se activa cuando un nodo es clickeado."""
        dialog = ContactDetailDialog(node_data, self)
        dialog.exec()

    def create_hud(self):
        hud_frame = QFrame()
        hud_frame.setObjectName("HUD")
        hud_layout = QHBoxLayout(hud_frame)
        
        # LÓGICA A IMPLEMENTAR:
        # Estos QLabels deben estar conectados a las variables de tu juego
        # para que se actualicen en cada turno.
        self.player_name_label = QLabel("Nombre Jugador: ")
        self.player_name_label.setStyleSheet("font-weight: bold;")
        self.capital_label = QLabel("Capital Político: 1,000,000")
        self.money_label = QLabel("Dinero Sucio: $500,000")
        self.influence_label = QLabel("Influencia: 250")
        self.suspicion_label = QLabel("Sospecha:")
        self.suspicion_bar = QProgressBar()
        self.suspicion_bar.setValue(10) # Valor de 0 a 100
        
        hud_layout.addWidget(self.player_name_label)
        hud_layout.addStretch() # Espaciador
        hud_layout.addWidget(self.capital_label)
        hud_layout.addWidget(self.money_label)
        hud_layout.addWidget(self.influence_label)
        hud_layout.addWidget(self.suspicion_label)
        hud_layout.addWidget(self.suspicion_bar)
        
        return hud_frame
    
    def update_player_name(self, name):
        self.player_name_label.setText(f"Nombre Jugador: {name}")

    def create_side_panel(self):
        side_panel_frame = QFrame()
        side_panel_frame.setObjectName("SidePanel")
        side_panel_layout = QVBoxLayout(side_panel_frame)
        side_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        side_panel_layout.setSpacing(15)
        
        actions_header = QLabel("ACCIONES ESTRATÉGICAS")
        actions_header.setObjectName("Header")
        
        # Botones de acción
        btn_expand = QPushButton("Expandir Red")
        btn_extract = QPushButton("Extraer Recursos")
        btn_cover_up = QPushButton("Operación de Encubrimiento")
        btn_neutralize = QPushButton("Neutralizar Amenaza")
        
        # Botón de Finalizar Turno
        btn_end_turn = QPushButton("FINALIZAR TURNO")
        btn_end_turn.setObjectName("GoldenButton")

        # Botón de prueba para la pantalla de derrota
        btn_test_defeat = QPushButton("Test Derrota")
        btn_test_defeat.clicked.connect(self.switch_to_defeat)

        # LÓGICA A IMPLEMENTAR:
        # Conectar cada botón a su función correspondiente en la lógica del juego.
        # btn_expand.clicked.connect(self.expand_network_logic)
        # btn_extract.clicked.connect(self.extract_resources_logic)
        # etc...
        # btn_end_turn.clicked.connect(self.process_turn_logic)
        
        side_panel_layout.addWidget(actions_header)
        side_panel_layout.addWidget(btn_expand)
        side_panel_layout.addWidget(btn_extract)
        side_panel_layout.addWidget(btn_cover_up)
        side_panel_layout.addWidget(btn_neutralize)
        side_panel_layout.addStretch() # Empuja el botón de turno hacia abajo
        side_panel_layout.addWidget(btn_test_defeat) # Botón de prueba
        side_panel_layout.addWidget(btn_end_turn)
        
        return side_panel_frame

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
        
        # LÓGICA A IMPLEMENTAR:
        # El texto de este QLabel debería ser dinámico, basado en la causa de la derrota.
        self.reason_label = QLabel("Causa: El Nivel de Sospecha ha alcanzado el 100%. La Fiscalía ha emitido una orden de captura.")
        self.reason_label.setWordWrap(True)
        self.reason_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        back_to_menu_button = QPushButton("VOLVER AL MENÚ PRINCIPAL")
        back_to_menu_button.clicked.connect(switch_to_main_menu)
        
        layout.addWidget(title)
        layout.addWidget(self.reason_label)
        layout.addSpacing(30)
        layout.addWidget(back_to_menu_button, alignment=Qt.AlignmentFlag.AlignCenter)
