from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from modelo.entidades.NodeData import NodeData

# --- NUEVA VENTANA DE DETALLES DEL CONTACTO ---
class ContactDetailDialog(QDialog):
    def __init__(self, node_data: NodeData, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Expediente del Contacto")
        self.setMinimumWidth(800)

        # --- Layout Principal ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Columna Izquierda ---
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        profile_pic_label = QLabel()
        pixmap = QPixmap(node_data.image_path).scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        profile_pic_label.setPixmap(pixmap)
        profile_pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        name_label = QLabel(node_data.name)
        name_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        level_label = QLabel(node_data.level)
        level_label.setStyleSheet("color: #AAAAAA;")
        level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout.addWidget(profile_pic_label)
        left_layout.addWidget(name_label)
        left_layout.addWidget(level_label)
        left_layout.addSpacing(20)

        ability_frame = QFrame()
        ability_layout = QHBoxLayout(ability_frame)
        ability_icon = QLabel()
        ability_icon.setPixmap(QPixmap("vista/assets/images/ability_icon.png").scaled(24, 24))
        ability_text = QLabel(node_data.special_ability)
        ability_layout.addWidget(ability_icon)
        ability_layout.addWidget(ability_text)
        left_layout.addWidget(ability_frame)

        # --- Columna Derecha ---
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        status_label = QLabel(f"Estado: {node_data.status}")
        status_colors = {
            'Activo': 'background-color: #2E7D32; color: white;',
            'Bajo Sospecha': 'background-color: #F9A825; color: black;',
            'Investigado': 'background-color: #C62828; color: white;',
            'Quemado': 'background-color: #424242; color: #AAAAAA;'
        }
        status_label.setStyleSheet(f"padding: 5px; border-radius: 5px; {status_colors.get(node_data.status, '')}")
        
        loyalty_bar = QProgressBar()
        loyalty_bar.setObjectName("LoyaltyBar")
        loyalty_bar.setFormat(f"Lealtad: {node_data.loyalty}%")
        loyalty_bar.setValue(node_data.loyalty)

        ambition_bar = QProgressBar()
        ambition_bar.setObjectName("AmbitionBar")
        ambition_bar.setFormat(f"Ambición: {node_data.ambition}%")
        ambition_bar.setValue(node_data.ambition)
        
        risk_bar = QProgressBar()
        risk_bar.setFormat(f"Riesgo: {node_data.risk}%")
        risk_bar.setValue(node_data.risk)
        
        bribe_label = QLabel(f"Costo Soborno: ${node_data.bribe_cost:,}")
        influence_label = QLabel(f"Aporte Influencia: {node_data.influence_gen} pts/turno")
        wealth_label = QLabel(f"Aporte Riqueza: ${node_data.wealth_gen:,}/turno")

        right_layout.addWidget(status_label)
        right_layout.addSpacing(15)
        right_layout.addWidget(loyalty_bar)
        right_layout.addWidget(ambition_bar)
        right_layout.addWidget(risk_bar)
        right_layout.addSpacing(15)
        right_layout.addWidget(bribe_label)
        right_layout.addWidget(influence_label)
        right_layout.addWidget(wealth_label)

        # Añadir paneles al layout principal
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        main_layout.addWidget(self.create_side_panel(), 1)

    @staticmethod
    def create_side_panel():
        side_panel_frame = QFrame()
        side_panel_frame.setObjectName("SidePanel")
        side_panel_layout = QVBoxLayout(side_panel_frame)
        side_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        side_panel_layout.setSpacing(15)
        
        actions_header = QLabel("ACCIONES ESTRATÉGICAS")
        actions_header.setObjectName("Header")
        
        btn_expand = QPushButton("Expandir Red")
        btn_extract = QPushButton("Extraer Recursos")
        btn_cover_up = QPushButton("Operación de Encubrimiento")
        btn_neutralize = QPushButton("Neutralizar Amenaza")
        

        side_panel_layout.addWidget(actions_header)
        side_panel_layout.addWidget(btn_expand)
        side_panel_layout.addWidget(btn_extract)
        side_panel_layout.addWidget(btn_cover_up)
        side_panel_layout.addWidget(btn_neutralize)
        side_panel_layout.addStretch()
        
        return side_panel_frame