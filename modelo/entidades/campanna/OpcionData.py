from dataclasses import dataclass

@dataclass
class OpcionData:
    """Representa una opción dentro de un PopUp."""
    texto: str
    respuesta: str
