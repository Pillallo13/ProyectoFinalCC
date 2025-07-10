from modelo.entidades.campanna.EventosData import OpcionData
from dataclasses import dataclass, field
from typing import List


@dataclass
class PopUpData:
    """Representa un PopUp dentro de un evento, con un personaje y texto."""
    personaje: str
    texto: str
    opciones: List["OpcionData"] = field(default_factory=list)