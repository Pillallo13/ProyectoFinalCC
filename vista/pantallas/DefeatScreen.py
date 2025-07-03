from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *


class DefeatScreen(QWidget):
    def __init__(self, switch_to_main_menu):
        super().__init__()  # ← llama al constructor de QWidget
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
