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

            # Imprimir el primer elemento de la lista para inspeccionar la estructura
            print(data[0])  # Esta línea te permitirá ver cómo está estructurado el primer objeto de la lista

            # Ajustar el acceso a las claves según la estructura real de data[0]
            personaje_data = {
                "nombre_completo": data[0].get("nombre", "Nombre no disponible"),  # Cambia "nombre" por "nombre_completo"
                "fecha_nacimiento": data[0].get("fecha_nacimiento", "Fecha no disponible"),
                "lugar_nacimiento": data[0].get("lugar_nacimiento", "Lugar no disponible"),
                "profesion": data[0].get("profesion", "Profesión no disponible"),
                "partido_politico": data[0].get("partido_politico", "Partido no disponible")
            }

            # Crear el objeto PersonajeData usando los datos
            self._personaje = PersonajeData(**personaje_data)

            # Verificar si la clave 'hechos_importantes' existe en el primer elemento
            if "hechos_importantes" in data[0]:
                # Cargar eventos como lista de dataclasses desde "hechos_importantes"
                self._eventos = [
                    EventoData(
                        año=e["año"],
                        evento=e["evento"],
                        impacto=e["impacto"],
                        PopUp=e.get("PopUp", {}),
                        textoDerrota=e["textoDerrota"]
                    )
                    for e in data[0]["hechos_importantes"]
                ]
            else:
                print("No se encontró la clave 'hechos_importantes' en el JSON.")

    def get_personaje(self):
        return self._personaje

    def obtener_nombre_jugador(self):
        """Devuelve el nombre completo del jugador directamente desde el JSON."""
        return self._personaje.nombre_completo  # Asegúrate de que esto sea consistente con la clase

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
