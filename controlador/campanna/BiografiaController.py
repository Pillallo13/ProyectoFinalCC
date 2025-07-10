import os
import json
from modelo.entidades.campanna.PersonajeData import PersonajeData
from modelo.entidades.campanna.EventosData import EventoData

class BiografiaController:
    def __init__(self, path_json=None):
        if path_json is None:
            # base_dir = carpeta actual
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir dos niveles para encontrar el archivo JSON
            path_json = os.path.normpath(
                os.path.join(base_dir, "..", "..", "modelo", "datos", "campanna", "redPoliticaCampana.json"))

        self.path_json = path_json
        self._personaje = None
        self._eventos = []
        self._cargar_datos()

    def _cargar_datos(self):
        with open(self.path_json, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Cargar el personaje como dataclass
            self._personaje = PersonajeData(**data["personaje"])

            # Cargar eventos como lista de dataclasses
            self._eventos = [
                EventoData(id_evento=e["id_evento"], texto=e["texto"])
                for e in data["relato"]
            ]

    def get_personaje(self):
        return self._personaje

    def obtener_nombre_jugador(self):
        """Devuelve el nombre completo del jugador directamente desde el JSON."""
        return self._personaje.nombre_completo  # Acceder como atributo de la instancia, no como un diccionario

    def buscar_evento_por_id(self, id_evento: str):
        """
        Retorna el evento que coincide con el ID proporcionado.

        Args:
            id_evento (str): Identificador del evento (ej. 'evento1').

        Returns:
            EventosData | None: El evento encontrado o None si no existe.
        """
        for evento in self._eventos:
            if evento.id_evento == id_evento:
                return evento
        return None
