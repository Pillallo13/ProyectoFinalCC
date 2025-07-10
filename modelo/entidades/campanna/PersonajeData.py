from modelo.entidades.campanna.EventosData import EventoData
from dataclasses import dataclass, field
from typing import List


@dataclass
class PersonajeData:
    """Contiene la información básica de un personaje político o histórico."""
    nombre_completo: str
    fecha_nacimiento: str
    lugar_nacimiento: str
    profesion: str
    partido_politico: str
    hechos_importantes: List["EventoData"] = field(default_factory=list)  # Lista de eventos importantes

    def agregar_evento(self, evento: "EventoData"):
        """
        Agrega un evento a la lista de hechos importantes del personaje.
        """
        self.hechos_importantes.append(evento)
