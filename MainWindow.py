import sys
from PyQt6.QtWidgets import (QApplication,QMainWindow,QStackedWidget)
from PyQt6.QtGui import QFontDatabase

# Importaciones de vistas y pantallas
from vista.pantallas.elementosGlobales.DefeatScreen import DefeatScreen
from vista.pantallas.elementosGlobales.GameModeSelection import GameModeSelection
from vista.pantallas.ModoCampaña.MainGameHistoriaUI import MainGameHistoriaUI
from vista.pantallas.MainMenu import MainMenu

# --- VENTANA PRINCIPAL (GESTOR DE VISTAS) ---
class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    Este componente gestiona la navegación entre las diferentes vistas del juego
    utilizando un QStackedWidget. Las vistas incluyen el menú principal, la selección
    de modo de juego, la interfaz de juego principal y la pantalla de derrota.

    Atributos:
        player_name (str): Nombre del jugador ingresado en el diálogo inicial.
        stacked_widget (QStackedWidget): Contenedor de las vistas que se alternan.
        main_menu (MainMenu): Vista del menú principal.
        game_mode_selection (GameModeSelection): Pantalla de selección de modo.
        main_game_ui (MainGameHistoriaUI): Vista principal del juego en modo campaña.
        defeat_screen (DefeatScreen): Pantalla que se muestra al perder.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, carga las fuentes personalizadas, crea las
        vistas y configura el sistema de navegación.
        """
        super().__init__()
        self.setWindowTitle("Corruptópolis")
        self.setGeometry(100, 100, 1280, 720)

        # Cargar tipografías personalizadas
        QFontDatabase.addApplicationFont("vista/assets/fonts/Roboto_Regular.ttf")
        QFontDatabase.addApplicationFont("vista/assets/fonts/Roboto_Condensed-Bold.ttf")

        # Nombre del jugador (se definirá luego del diálogo)
        self.player_name = ""

        # Contenedor de vistas apiladas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Instanciar cada vista
        self.main_menu = MainMenu(self.switch_to_mode_selection)
        self.game_mode_selection = GameModeSelection(self.switch_to_game)
        self.main_game_ui = MainGameHistoriaUI(self.switch_to_defeat)
        self.defeat_screen = DefeatScreen(self.switch_to_main_menu)

        # Añadir vistas al stack
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.game_mode_selection)
        self.stacked_widget.addWidget(self.main_game_ui)
        self.stacked_widget.addWidget(self.defeat_screen)

        # Cargar estilos visuales
        self.load_stylesheet()

        # Mostrar el menú principal al inicio
        self.switch_to_main_menu()

    def load_stylesheet(self):
        """
        Carga la hoja de estilos personalizada (QSS).
        Si no se encuentra, muestra un aviso y continúa con estilos por defecto.
        """
        try:
            with open("vista/assets/styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo styles.qss no encontrado. Se usará el estilo por defecto.")

    def switch_to_main_menu(self):
        """
        Cambia la vista activa al menú principal.
        """
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def switch_to_mode_selection(self):
        """
        Cambia la vista activa a la pantalla de selección de modo de juego.
        """
        self.stacked_widget.setCurrentWidget(self.game_mode_selection)

    def switch_to_game(self, mode, player_name=None):
        """
        Cambia la vista activa a la interfaz de juego principal y actualiza el nombre del jugador.

        Args:
            mode (str): Identificador del modo de juego seleccionado ('campaign', 'infinite', 'multiplayer').
            player_name (str | None): Nombre ingresado por el jugador. Si es None, se mantiene el anterior.
        """
        if player_name:
            self.player_name = player_name
        self.main_game_ui.update_player_name()
        self.stacked_widget.setCurrentWidget(self.main_game_ui)

    def switch_to_defeat(self):
        """
        Cambia la vista activa a la pantalla de derrota.
        """
        self.stacked_widget.setCurrentWidget(self.defeat_screen)


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
