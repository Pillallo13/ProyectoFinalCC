from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from vista.ventana.PlayerNameDialog import PlayerNameDialog


class GameModeSelection(QWidget):
    """
    Vista de selección de modo de juego.

    Esta pantalla se muestra luego del menú principal y permite al jugador elegir
    entre tres modos de juego: campaña, infinito y multijugador.

    Cada modo está representado como una tarjeta con un título y una descripción.
    El jugador puede hacer clic en una tarjeta para iniciar el juego en ese modo.

    Atributos:
        background_image (QPixmap): Imagen de fondo que se dibuja en paintEvent.
    """

    def __init__(self, switch_to_game, parent=None):
        """
        Inicializa la pantalla de selección de modo de juego.

        Args:
            switch_to_game (callable): Función del controlador que se invoca al
                seleccionar un modo de juego. Recibe como parámetro un string con
                el identificador del modo (por ejemplo: 'campaign', 'infinite', etc.).
        """
        super().__init__(parent)
        self.setObjectName("GameModeSelection")  # Para aplicar estilos desde el QSS

        # Carga la imagen de fondo que se usará al repintar la ventana
        self.background_image = QPixmap("vista/assets/images/imagen_background.png")

        # Layout principal vertical que organiza el contenido de la pantalla
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título principal de la pantalla
        header = QLabel("SELECCIONAR MODO DE JUEGO")
        header.setObjectName("Header")  # Estilo definido en stylesheet
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        main_layout.addSpacing(50)  # Espacio entre título y tarjetas

        # Layout horizontal que contendrá las tarjetas de modo de juego
        cards_layout = QHBoxLayout()
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cards_layout.setSpacing(40)

        # Tarjeta para el modo campaña
        campaign_card = self.create_mode_card(
            "LA ESCALERA AL PODER",
            "Sigue una narrativa con objetivos progresivos, desde concejal hasta la presidencia.",
            lambda: switch_to_game("campaign")  # Se llama con el modo al hacer clic
        )

        # Tarjeta para el modo infinito
        infinite_card = self.create_mode_card(
            "IMPERIO INFINITO",
            "Sobrevive el mayor tiempo posible mientras la dificultad aumenta. El objetivo es la máxima puntuación.",
            lambda: self.pedir_nombre_y_continuar(switch_to_game, "campaign")
        )

        # Tarjeta para el modo multijugador
        multiplayer_card = self.create_mode_card(
            "GUERRA DE CARTELES",
            "Compite contra otros jugadores por el control del territorio político. (Multijugador Local)",
            lambda: self.pedir_nombre_y_continuar(switch_to_game, "campaign")
        )

        # Añadir las tarjetas al layout horizontal
        cards_layout.addWidget(campaign_card)
        cards_layout.addWidget(infinite_card)
        cards_layout.addWidget(multiplayer_card)

        # Añadir el layout de tarjetas al layout principal
        main_layout.addLayout(cards_layout)

        # Establecer el layout principal como el layout de este widget
        self.setLayout(main_layout)

    def create_mode_card(self, title_text, desc_text, on_click_action):
        """
        Crea una tarjeta interactiva (card) para un modo de juego.

        Args:
            title_text (str): Título que representa el nombre del modo.
            desc_text (str): Descripción del modo que se muestra debajo del título.
            on_click_action (callable): Función a ejecutar cuando se hace clic en la tarjeta.

        Returns:
            QFrame: Tarjeta lista para ser añadida a un layout.
        """
        card = QFrame(self)
        card.setObjectName("Card")  # Se aplica estilo específico por ID
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setCursor(Qt.CursorShape.PointingHandCursor)  # Estilo visual del cursor al pasar

        # Layout vertical interno de la tarjeta
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título del modo (ej: 'LA ESCALERA AL PODER')
        title = QLabel(title_text)
        title.setStyleSheet("color: #FFC107; font-weight: bold; font-size: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Descripción del modo, con salto de línea si es necesario
        description = QLabel(desc_text)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir título y descripción al layout de la tarjeta
        card_layout.addWidget(title)
        card_layout.addSpacing(15)
        card_layout.addWidget(description)

        # Asignar el evento de clic del mouse a la acción proporcionada
        card.mousePressEvent = lambda event: on_click_action()

        return card

    def paintEvent(self, event):
        """
        Evento de repintado de la vista.

        Dibuja la imagen de fondo en todo el rectángulo del widget
        cada vez que se actualiza visualmente la pantalla.

        Args:
            event (QPaintEvent): Evento interno de Qt que solicita redibujo.
        """
        painter = QPainter(self)
        # Dibuja el fondo escalado para cubrir toda la ventana
        painter.drawPixmap(self.rect(), self.background_image)
        # Llama al evento original por si hay contenido adicional
        super().paintEvent(event)

    def pedir_nombre_y_continuar(self, callback, modo):
        dialog = PlayerNameDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre = dialog.get_player_name() or "Anónimo"
            callback(modo, nombre)

