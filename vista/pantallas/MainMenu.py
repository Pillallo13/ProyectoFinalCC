from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from vista.resources import IMAGES


# --- VISTA 1: MENÚ PRINCIPAL (MODIFICADO) ---
class MainMenu (QWidget):
    def __init__(self, start_new_game_flow):
        super().__init__()
        self.setObjectName("MainMenu")
        self.background_image = QPixmap(str(IMAGES["background_menu"]))
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Corruptópolis")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("El Ascenso y Caída en el Laberinto del Poder")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        new_game_button = QPushButton("NUEVA PARTIDA")
        loadGame_button = QPushButton("Cargar partida")
        exit_button = QPushButton("SALIR")
        
        new_game_button.clicked.connect(start_new_game_flow)
        exit_button.clicked.connect(QApplication.instance().quit)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(50)
        layout.addWidget(new_game_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(loadGame_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    # --- METODO MODIFICADO PARA DIBUJAR EL FONDO ---
    def paintEvent(self, event):
        painter = QPainter(self)
        # Dibuja la imagen de fondo, escalada para llenar toda la ventana
        painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)