from modelo.entidades.NodeData import NodeData
import os

class NodoController:
    def __init__(self, path_json=None):
        if path_json is None:
            # base_dir = carpeta actual (red_politica)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # subir dos niveles: red_politica → controlador → raíz
            path_json = os.path.normpath(os.path.join(base_dir, "../../modelo/datos/redPolitica.json"))

        self.path_json = path_json
        self.nodos: list[NodeData] = NodeData.cargar_desde_json(path_json)

    def buscar_por_id(self, nodo_id: int) -> NodeData | None:
        for nodo in self.nodos:
            if nodo.id == nodo_id:
                return nodo
        return None

    def obtener_todos(self) -> list[NodeData]:
        return self.nodos
