from dataclasses import dataclass, field
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# --- VISTA 2: SELECCIÓN DE MODO DE JUEGO ---
class GameModeSelection(QWidget):
    def __init__(self, switch_to_game):
        super().__init__()
        self.setObjectName("GameModeSelection")
        self.background_image = QPixmap("vista/assets/images/imagen_background.png")
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        header = QLabel("SELECCIONAR MODO DE JUEGO")
        header.setObjectName("Header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        main_layout.addSpacing(50)
        
        cards_layout = QHBoxLayout()
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cards_layout.setSpacing(40)

        # Crear y añadir las tarjetas de modo de juego
        campaign_card = self.create_mode_card(
            "LA ESCALERA AL PODER",
            "Sigue una narrativa con objetivos progresivos, desde concejal hasta la presidencia.",
            lambda: switch_to_game("campaign")
        )
        infinite_card = self.create_mode_card(
            "IMPERIO INFINITO",
            "Sobrevive el mayor tiempo posible mientras la dificultad aumenta. El objetivo es la máxima puntuación.",
            lambda: switch_to_game("infinite")
        )
        multiplayer_card = self.create_mode_card(
            "GUERRA DE CARTELES",
            "Compite contra otros jugadores por el control del territorio político. (Multijugador Local)",
            lambda: switch_to_game("multiplayer")
        )
        
        cards_layout.addWidget(campaign_card)
        cards_layout.addWidget(infinite_card)
        cards_layout.addWidget(multiplayer_card)
        
        main_layout.addLayout(cards_layout)
        self.setLayout(main_layout)

    def create_mode_card(self, title_text, desc_text, on_click_action):
        card = QFrame()
        card.setObjectName("Card")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = QLabel(title_text)
        title.setStyleSheet("color: #FFC107; font-weight: bold; font-size: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel(desc_text)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(title)
        card_layout.addSpacing(15)
        card_layout.addWidget(description)
        
        card.mousePressEvent = lambda event: on_click_action()

        return card
        
    def paintEvent(self, event):
        painter = QPainter(self)
        # Dibuja la imagen de fondo, escalada para llenar toda la ventana
        painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)

    