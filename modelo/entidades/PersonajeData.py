from dataclasses import dataclass

@dataclass
class PersonajeData:
    """Contiene la información básica de un personaje político o histórico."""
    nombre_completo: str
    fecha_nacimiento: str
    lugar_nacimiento: str
    profesion: str