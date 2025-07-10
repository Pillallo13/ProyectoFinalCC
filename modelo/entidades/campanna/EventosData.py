from modelo.entidades.campanna.OpcionData import OpcionData
from modelo.entidades.campanna.PopUpData import PopUpData
from dataclasses import dataclass, field
from typing import List, Optional



@dataclass
class EventoData:
    """Representa un evento o hito dentro de la biografía del personaje."""
    año: int
    evento: str
    impacto: str
    texto: str
    textoDerrota: Optional[str] = None
    PopUp: Optional["PopUpData"] = None  # Relación a PopUpData si existe
    opciones: List["OpcionData"] = field(default_factory=list)  # Lista de opciones del PopUp