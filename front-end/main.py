import sys
from dataclasses import dataclass, field
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QFrame, QProgressBar, QDialog, QLineEdit,
                             QDialogButtonBox, QGraphicsView, QGraphicsScene,
                             QGraphicsObject, QGraphicsLineItem)
from PyQt6.QtGui import (QFont, QFontDatabase, QIcon, QPixmap, QPainter, QPalette, 
                         QBrush, QColor, QPen)
from PyQt6.QtCore import Qt, QSize, QRectF, pyqtSignal, QPointF, QLineF

# --- VISTAS ---
# Importar las vistas desde sus respectivos archivos
from vista_menu_principal import MainMenu, PlayerNameDialog
from vista_modo_juego import GameModeSelection
from vista_principal_juego import MainGameUI, DefeatScreen

# --- ESTILOS (QSS - Similar a CSS) ---
# En un proyecto más grande, esto iría en un archivo styles.qss separado.
STYLESHEET = """
QWidget#MainMenu, QWidget#GameModeSelection, QWidget#DefeatScreen, QDialog {
    background-color: #1A1A1A;
}
QWidget#MainGameUI {
    background-color: #1A1A1A;
}
QLabel {
    color: #E0E0E0;
    font-family: 'Roboto';
    font-size: 16px;
}
QLabel#Title {
    font-family: 'Roboto Condensed'; font-size: 48px; font-weight: bold; color: #E0E0E0;
    background-color: rgba(0, 0, 0, 0.5); padding: 10px; border-radius: 5px;
}
QLabel#Subtitle {
    font-family: 'Roboto'; font-size: 18px; color: #AAAAAA;
    background-color: rgba(0, 0, 0, 0.5); padding: 5px; border-radius: 5px;
}
QLabel#Header {
    font-family: 'Roboto Condensed'; font-size: 28px; font-weight: bold; color: #E0E0E0;
}
QPushButton {
    background-color: #2C2C2C; border: 1px solid #888888; color: #E0E0E0;
    padding: 12px; font-family: 'Roboto Condensed'; font-size: 16px;
    font-weight: bold; min-width: 200px;
}
QPushButton:hover {
    border: 1px solid #FFC107; color: #FFC107;
}
QPushButton:pressed {
    background-color: #FFC107; color: #1A1A1A;
}
QPushButton#GoldenButton {
    background-color: #FFC107; color: #1A1A1A; border: none;
}
QPushButton#GoldenButton:hover {
    background-color: #ffca2c;
}
QFrame#Card, QFrame#HUD, QFrame#SidePanel {
    background-color: #2C2C2C; border-radius: 8px;
}
QFrame#Card:hover {
    border: 1px solid #FFC107;
}
QLineEdit {
    background-color: #444; border: 1px solid #888; padding: 8px;
    color: #E0E0E0; font-size: 16px; border-radius: 5px;
}
QProgressBar {
    border: 1px solid #555; border-radius: 5px; text-align: center;
    color: #E0E0E0; background-color: #444; height: 22px;
}
QProgressBar::chunk {
    background-color: #D32F2F; border-radius: 4px; /* Rojo Peligro por defecto */
}
/* Barras de progreso con colores específicos */
QProgressBar#LoyaltyBar::chunk { background-color: #FFC107; } /* Dorado */
QProgressBar#AmbitionBar::chunk { background-color: #9C27B0; } /* Púrpura */
QGraphicsView { border: none; background-color: #111; }
"""

# --- VENTANA PRINCIPAL (GESTOR DE VISTAS - MODIFICADO) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corruptópolis")
        self.setGeometry(100, 100, 1280, 720)
        
        QFontDatabase.addApplicationFont("fonts/Roboto_Regular.ttf")
        QFontDatabase.addApplicationFont("fonts/Roboto_Condensed-Bold.ttf")

        self.player_name = "" # Variable para guardar el nombre del jugador

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.main_menu = MainMenu(self.prompt_for_player_name) # Conectado al nuevo flujo
        self.game_mode_selection = GameModeSelection(self.switch_to_game)
        self.main_game_ui = MainGameUI(self.switch_to_defeat)
        self.defeat_screen = DefeatScreen(self.switch_to_main_menu)
        
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.game_mode_selection)
        self.stacked_widget.addWidget(self.main_game_ui)
        self.stacked_widget.addWidget(self.defeat_screen)
        
        self.setStyleSheet(STYLESHEET)
        self.switch_to_main_menu()

    def prompt_for_player_name(self):
        dialog = PlayerNameDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.player_name = dialog.get_player_name()
            if not self.player_name: # Si no ingresó nada, poner un default
                self.player_name = "Anónimo"
            self.switch_to_mode_selection()

    def switch_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def switch_to_mode_selection(self):
        self.stacked_widget.setCurrentWidget(self.game_mode_selection)

    def switch_to_game(self, mode):
        print(f"Iniciando juego en modo: {mode} para el jugador: {self.player_name}")
        # Actualizar el nombre en la UI del juego
        self.main_game_ui.update_player_name(self.player_name)
        self.stacked_widget.setCurrentWidget(self.main_game_ui)
    
    def switch_to_defeat(self):
        self.stacked_widget.setCurrentWidget(self.defeat_screen)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())