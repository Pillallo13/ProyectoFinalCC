import json
import os

from modelo.entidades.campanna.EventosData import EventoData
from modelo.entidades.campanna.OpcionData import OpcionData
from modelo.entidades.campanna.PersonajeData import PersonajeData
from modelo.entidades.campanna.PopUpData import PopUpData  # Si es necesario, importar PopUpData y OpcionData


class PersonajeController:
    nombre_completo = None

    def __init__(self, path_json=None):
        if path_json is None:
            # Establece la ruta al archivo JSON
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path_json = os.path.normpath(
                os.path.join(base_dir, "..", "..", "modelo", "datos", "campanna", "biografia.json"))

        self.path_json = path_json
        self.personaje = self.cargar_desde_json(path_json)

    def cargar_desde_json(self, path: str) -> PersonajeData:
        """
        Carga los datos del personaje desde el archivo JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Crear el personaje principal
        personaje = PersonajeData(
            nombre_completo=data["nombre"],
            fecha_nacimiento=data["fecha_nacimiento"],
            lugar_nacimiento=data["lugar_nacimiento"],
            profesion=data["profesion"],
            partido_politico=data["partido_politico"]
        )

        # Crear los eventos
        for hecho in data["hechos_importantes"]:
            popup = None
            opciones = []

            if "PopUp" in hecho:
                popup = PopUpData(
                    personaje=hecho["PopUp"]["personaje"],
                    texto=hecho["PopUp"]["texto"]
                )
                for opcion in hecho["PopUp"]["opciones"]:
                    opciones.append(OpcionData(texto=opcion["texto"], respuesta=opcion["respuesta"]))

            evento = EventoData(
                año=hecho["año"],
                evento=hecho["evento"],
                impacto=hecho["impacto"],
                texto=hecho["evento"],
                textoDerrota=hecho.get("textoDerrota"),
                PopUp=popup,
                opciones=opciones
            )
            personaje.agregar_evento(evento)

        return personaje

    def obtener_personaje(self) -> PersonajeData:
        """
        Devuelve la información completa del personaje.
        """
        return self.personaje

    def getNombreCompleto(self) -> str:
        return self.personaje.nombre_completo

    def guardar_en_json(self):
        """
        Guarda los datos del personaje en el archivo JSON.
        """
        with open(self.path_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Actualizar los datos de los eventos
        data["hechos_importantes"] = [evento.__dict__ for evento in self.personaje.hechos_importantes]

        # Guardar los datos actualizados en el archivo
        with open(self.path_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)