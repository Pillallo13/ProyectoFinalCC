import os
from modelo.entidades.campanna.NodeData import NodeData

class NodoController:
    def __init__(self, path_json=None):
        if path_json is None:
            # base_dir = carpeta actual
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir dos niveles para encontrar el archivo JSON
            path_json = os.path.normpath(os.path.join(base_dir, "../modelo/datos/campanna/redPoliticaCampana.json"))

        self.path_json = path_json
        self.nodos: list[NodeData] = NodeData.cargar_desde_json(path_json)  # Carga los nodos desde el JSON

    def buscar_por_id(self, nodo_id: int) -> NodeData | None:
        """
        Busca un nodo por su ID.
        Args:
            nodo_id (int): El ID del nodo a buscar.
        Returns:
            NodeData | None: El nodo encontrado o None si no existe.
        """
        for nodo in self.nodos:
            if nodo.id == nodo_id:
                return nodo
        return None

    def obtener_todos(self) -> list[NodeData]:
        """
        Devuelve todos los nodos.
        """
        return self.nodos

    def comprar_nodo(self, nodo_id: int) -> bool:
        """
        Compra un nodo buscando por ID y establece su estado de compra si es posible.
        Args:
            nodo_id (int): El ID del nodo a comprar.
        Returns:
            bool: True si el nodo fue comprado correctamente, False si no.
        """
        nodo = self.buscar_por_id(nodo_id)
        if nodo and nodo.comprar():
            nodo.guardar_en_json(self.path_json)
            return True
        return False

    def establecer_relacion(self, nodo_comprador_id: int, nodo_comprado_id: int) -> bool:
        """
        Establece una relación de padre-hijo entre dos nodos.
        Args:
            nodo_comprador_id (int): El ID del nodo que compra.
            nodo_comprado_id (int): El ID del nodo que es comprado.
        Returns:
            bool: True si la relación fue establecida correctamente, False si no.
        """
        nodo_comprador = self.buscar_por_id(nodo_comprador_id)
        nodo_comprado = self.buscar_por_id(nodo_comprado_id)

        if nodo_comprador and nodo_comprado:
            nodo_comprador.agregar_relacion(nodo_comprado)
            nodo_comprador.guardar_en_json(self.path_json)
            nodo_comprado.guardar_en_json(self.path_json)
            return True
        return False
