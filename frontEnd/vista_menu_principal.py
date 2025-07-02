from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QFrame, QProgressBar, QDialog, QLineEdit,
                             QDialogButtonBox)
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QPixmap, QPainter, QPalette, QBrush
from PyQt6.QtCore import Qt, QSize


# --- VISTA 1: MENÚ PRINCIPAL (MODIFICADO) ---
class MainMenu(QWidget):
    def __init__(self, start_new_game_flow):
        super().__init__()
        self.setObjectName("MainMenu")
        self.background_image = QPixmap("frontEnd/images/imagen_background.png")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Corruptópolis")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("El Ascenso y Caída en el Laberinto del Poder")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        new_game_button = QPushButton("NUEVA PARTIDA")
        exit_button = QPushButton("SALIR")
        
        new_game_button.clicked.connect(start_new_game_flow)
        exit_button.clicked.connect(QApplication.instance().quit)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(50)
        layout.addWidget(new_game_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    # --- MÉTODO MODIFICADO PARA DIBUJAR EL FONDO ---
    def paintEvent(self, event):
        painter = QPainter(self)
        # Dibuja la imagen de fondo, escalada para llenar toda la ventana
        painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)

class PlayerNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Iniciar Nueva Partida")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        label = QLabel("Ingresa el nombre de tu cacique político:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ej: Francisco de Paula...")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(buttons)

    def get_player_name(self):
        return self.name_input.text()