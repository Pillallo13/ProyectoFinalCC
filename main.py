import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from vista.pantallas.DefeatScreen import DefeatScreen
from vista.pantallas.GameModeSelection import GameModeSelection
from vista.pantallas.MainGameUI import MainGameUI
from vista.pantallas.MainMenu import MainMenu
from vista.ventanaStats.PlayerNameDialog import PlayerNameDialog

# --- VENTANA PRINCIPAL (GESTOR DE VISTAS) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corruptópolis")
        self.setGeometry(100, 100, 1280, 720)

        QFontDatabase.addApplicationFont("vista/assets/fonts/Roboto_Regular.ttf")
        QFontDatabase.addApplicationFont("vista/assets/fonts/Roboto_Condensed-Bold.ttf")

        self.player_name = ""  # Nombre del jugador

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self.prompt_for_player_name)
        self.game_mode_selection = GameModeSelection(self.switch_to_game)
        self.main_game_ui = MainGameUI(self.switch_to_defeat)
        self.defeat_screen = DefeatScreen(self.switch_to_main_menu)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.game_mode_selection)
        self.stacked_widget.addWidget(self.main_game_ui)
        self.stacked_widget.addWidget(self.defeat_screen)

        self.load_stylesheet()
        self.switch_to_main_menu()

    def load_stylesheet(self):
        try:
            with open("vista/assets/styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo styles.qss no encontrado. Se usará el estilo por defecto.")

    def prompt_for_player_name(self):
        dialog = PlayerNameDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.player_name = dialog.get_player_name() or "Anónimo"
            self.switch_to_mode_selection()

    def switch_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def switch_to_mode_selection(self):
        self.stacked_widget.setCurrentWidget(self.game_mode_selection)

    def switch_to_game(self, mode):
        print(f"Iniciando juego en modo: {mode} para el jugador: {self.player_name}")
        self.main_game_ui.update_player_name(self.player_name)
        self.stacked_widget.setCurrentWidget(self.main_game_ui)

    def switch_to_defeat(self):
        self.stacked_widget.setCurrentWidget(self.defeat_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
