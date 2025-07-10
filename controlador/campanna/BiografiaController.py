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
                os.path.join(base_dir, "..", "..", "modelo", "datos", "campanna", "biografia.json"))

        self.path_json = path_json
        self._personaje = None
        self._eventos = []
        self._cargar_datos()

    def _cargar_datos(self):
        """
        Carga los datos del archivo JSON. Primero, intenta leer los datos,
        luego procesa el personaje y los eventos importantes. Si los datos no son válidos,
        se maneja el error.
        """
        try:
            with open(self.path_json, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Imprimir el primer elemento de la lista para inspeccionar la estructura
                print(data)  # Imprime toda la estructura del JSON para verificar que está bien cargado

                # Asegurarse de que `data` no esté vacío y de que tenga un formato correcto
                if not data:
                    print("Error: El archivo JSON está vacío.")
                    return

                # Obtener los datos del personaje
                personaje_data = {
                    "nombre_completo": data.get("nombre", "Nombre no disponible"),
                    "fecha_nacimiento": data.get("fecha_nacimiento", "Fecha no disponible"),
                    "lugar_nacimiento": data.get("lugar_nacimiento", "Lugar no disponible"),
                    "profesion": data.get("profesion", "Profesión no disponible"),
                    "partido_politico": data.get("partido_politico", "Partido no disponible")
                }

                # Crear el objeto PersonajeData usando los datos
                self._personaje = PersonajeData(**personaje_data)

                # Cargar eventos si existen
                if "hechos_importantes" in data:
                    self._eventos = [
                        EventoData(
                            año=e["año"],
                            evento=e["evento"],
                            impacto=e["impacto"],
                            PopUp=e.get("PopUp", {}),
                            textoDerrota=e["textoDerrota"]
                        )
                        for e in data["hechos_importantes"]
                    ]
                else:
                    print("No se encontró la clave 'hechos_importantes' en el JSON.")
        except FileNotFoundError:
            print(f"Error: El archivo no se encuentra en la ruta especificada: {self.path_json}")
        except json.JSONDecodeError:
            print("Error: El archivo JSON está mal formado.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def get_personaje(self):
        """Devuelve la información del personaje cargado."""
        return self._personaje

    def obtener_nombre_jugador(self):
        """Devuelve el nombre completo del jugador directamente desde el JSON."""
        if self._personaje:
            return self._personaje.nombre_completo
        else:
            return "Nombre no disponible"  # En caso de que no se haya cargado el personaje aún

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
