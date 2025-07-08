from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from vista.resources import IMAGES

class MainMenu(QWidget):
    """
    Vista principal del menú de inicio del juego.

    Presenta el título, subtítulo y tres botones:
    - 'Nueva Partida': inicia el flujo de creación de jugador y modo de juego.
    - 'Cargar partida': (a implementar) permitiría restaurar partidas previas.
    - 'Salir': cierra la aplicación.

    También dibuja un fondo personalizado al redibujar el widget.
    """

    def __init__(self, start_new_game_flow):
        """
        Inicializa el menú principal del juego.

        Args:
            start_new_game_flow (callable): función que inicia la lógica para empezar una nueva partida.
        """
        super().__init__()
        self.setObjectName("MainMenu")

        # Imagen de fondo cargada desde los recursos (IMAGES es un diccionario de rutas)
        self.background_image = QPixmap(str(IMAGES["background_menu"]))

        # Layout principal vertical centrado
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Título del juego ---
        title = QLabel("Corruptópolis")
        title.setObjectName("Title")  # para aplicarle estilo desde el QSS
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Subtítulo del juego ---
        subtitle = QLabel("El Ascenso y Caída en el Laberinto del Poder")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Botones de interacción ---
        new_game_button = QPushButton("NUEVA PARTIDA")       # Empieza nuevo juego
        loadGame_button = QPushButton("Cargar partida")      # (Placeholder)
        exit_button = QPushButton("SALIR")                   # Cierra la aplicación

        # Conexiones de eventos de clic
        new_game_button.clicked.connect(start_new_game_flow)
        exit_button.clicked.connect(QApplication.instance().quit)

        # Añadir widgets al layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(50)
        layout.addWidget(new_game_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(loadGame_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Asignar layout al widget
        self.setLayout(layout)

    def paintEvent(self, event):
        """
        Evento de repintado del menú principal.

        Dibuja la imagen de fondo escalada al tamaño del widget.
        Llama al metodo base para que se pinte el contenido normalmente.

        Args:
            event (QPaintEvent): evento de actualización visual de Qt.
        """
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)
