import json
import os
from typing import List, Optional
from modelo.entidades.campanna.EventosData import EventoData, PopUpData, OpcionData


class EventosController:
    def __init__(self, path_json=None):
        if path_json is None:
            # base_dir = carpeta actual
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir dos niveles para encontrar el archivo JSON
            path_json = os.path.normpath(os.path.join(base_dir, "../../modelo/datos/biografia.json"))

        self.path_json = path_json
        self.eventos: List[EventoData] = self.cargar_desde_json(path_json)  # Carga los eventos desde el JSON

    @staticmethod
    def cargar_desde_json(path: str) -> List[EventoData]:
        """
        Carga los eventos desde el archivo JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        eventos = []
        for raw in raw_data["hechos_importantes"]:
            popup = None
            opciones = []

            if "PopUp" in raw:
                popup = PopUpData(
                    personaje=raw["PopUp"]["personaje"],
                    texto=raw["PopUp"]["texto"]
                )
                for opcion in raw["PopUp"]["opciones"]:
                    opciones.append(OpcionData(texto=opcion["texto"], respuesta=opcion["respuesta"]))

            evento = EventoData(
                año=raw["año"],
                evento=raw["evento"],
                impacto=raw["impacto"],
                texto=raw["evento"],
                textoDerrota=raw.get("textoDerrota"),
                PopUp=popup,
                opciones=opciones
            )
            eventos.append(evento)

        return eventos

    def obtener_evento_por_año(self, año: int) -> Optional[EventoData]:
        """
        Obtiene un evento por su año.
        """
        for evento in self.eventos:
            if evento.año == año:
                return evento
        return None

    def guardar_en_json(self):
        """
        Guarda todos los eventos en el archivo JSON.
        """
        with open(self.path_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["hechos_importantes"] = [evento.__dict__ for evento in self.eventos]

        with open(self.path_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
