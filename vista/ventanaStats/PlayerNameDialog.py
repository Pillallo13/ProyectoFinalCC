from PyQt6.QtWidgets import *
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
