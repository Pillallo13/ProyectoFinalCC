from dataclasses import dataclass

@dataclass
class EventosData:
    """Representa un evento o hito dentro de la biografía del personaje."""
    id_evento: str
    texto: str
