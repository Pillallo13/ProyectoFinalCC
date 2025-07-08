from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *


class DefeatScreen(QWidget):
    """
    Vista de pantalla final que se muestra cuando el jugador es derrotado.

    Esta pantalla informa al jugador que ha perdido la partida debido al
    nivel máximo de sospecha o alguna otra causa crítica, y le permite
    regresar al menú principal mediante un botón de navegación.

    Atributos:
        reason_label (QLabel): Etiqueta que muestra la razón de la derrota.
    """

    def __init__(self, switch_to_main_menu):
        """
        Inicializa los elementos visuales de la pantalla de derrota.

        Args:
            switch_to_main_menu (callable): Función que permite regresar al
                menú principal. Es pasada por el controlador (MainWindow)
                y se ejecuta cuando el jugador presiona el botón de retorno.
        """
        super().__init__()
        self.setObjectName("DefeatScreen")

        # Layout principal que organiza los elementos de forma vertical
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Título grande que representa el estado de derrota
        title = QLabel("CAÍDA EN DESGRACIA")
        title.setStyleSheet(
            "color: #D32F2F; font-size: 48px; font-weight: bold; font-family: 'Roboto Condensed';"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Etiqueta que describe la causa de la derrota del jugador
        self.reason_label = QLabel(
            "Causa: El Nivel de Sospecha ha alcanzado el 100%. "
            "La Fiscalía ha emitido una orden de captura."
        )
        self.reason_label.setWordWrap(True)
        self.reason_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón que permite regresar al menú principal del juego
        back_to_menu_button = QPushButton("VOLVER AL MENÚ PRINCIPAL")
        back_to_menu_button.clicked.connect(switch_to_main_menu)

        # Añadir todos los elementos al layout principal
        layout.addWidget(title)
        layout.addWidget(self.reason_label)
        layout.addSpacing(30)
        layout.addWidget(back_to_menu_button, alignment=Qt.AlignmentFlag.AlignCenter)
