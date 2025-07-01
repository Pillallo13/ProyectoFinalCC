import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QFrame, QProgressBar, QDialog, QLineEdit,
                             QDialogButtonBox, QGraphicsView, QGraphicsScene,
                             QGraphicsObject, QGraphicsLineItem)
from PyQt6.QtGui import (QFont, QFontDatabase, QIcon, QPixmap, QPainter, QPalette, 
                         QBrush, QColor, QPen)
from PyQt6.QtCore import Qt, QSize, QRectF, pyqtSignal, QPointF, QLineF
from nodo import NodeData  

# --- NUEVA VENTANA DE DETALLES DEL CONTACTO ---
class ContactDetailDialog(QDialog):
    def __init__(self, node_data: NodeData, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Expediente del Contacto")
        self.setMinimumWidth(600)

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
        ability_icon.setPixmap(QPixmap("images/ability_icon.png").scaled(24, 24))
        ability_text = QLabel(node_data.special_ability)
        ability_layout.addWidget(ability_icon)
        ability_layout.addWidget(ability_text)
        left_layout.addWidget(ability_frame)


        # --- Columna Derecha ---
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Estado
        status_label = QLabel(f"Estado: {node_data.status}")
        status_colors = {
            'Activo': 'background-color: #2E7D32; color: white;',
            'Bajo Sospecha': 'background-color: #F9A825; color: black;',
            'Investigado': 'background-color: #C62828; color: white;',
            'Quemado': 'background-color: #424242; color: #AAAAAA;'
        }
        status_label.setStyleSheet(f"padding: 5px; border-radius: 5px; {status_colors.get(node_data.status, '')}")
        
        # Barras de Progreso
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
        
        # Otros datos
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

# --- NODO GRÁFICO PERSONALIZADO ---
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
        # Define el área clickeable y de dibujado del nodo
        return QRectF(-40, -40, 80, 80)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibuja el círculo del nodo
        pen_color = self.status_colors.get(self.node_data.status, QColor("white"))
        pen = QPen(pen_color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#2C2C2C")))
        painter.drawEllipse(-35, -35, 70, 70)
        
        # Dibuja el nombre debajo del nodo
        font = QFont("Roboto", 10)
        painter.setFont(font)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, self.node_data.name)

    def mousePressEvent(self, event):
        # Emite una señal con sus datos cuando se le hace clic
        self.node_clicked.emit(self.node_data)
        super().mousePressEvent(event)
