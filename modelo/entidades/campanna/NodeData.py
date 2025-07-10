import json
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class NodeData:
    id: int
    name: str
    level: str
    bribe_cost: int
    influence_gen: int
    wealth_gen: int
    loyalty: int
    ambition: int
    risk: int
    special_ability: str
    status: str
    acepta_sobornos: bool
    parent_id: Optional[int]
    subordinados: list[int]
    image_path: str
    moral: int = 0
    connected_to: list[dict] = field(default_factory=list)

    @staticmethod
    def cargar_desde_json(path: str) -> list["NodeData"]:
        """
        Carga los nodos desde un archivo JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        nodos = []
        for raw in raw_data:
            connected_to = raw.get("connected_to", [])
            if connected_to and isinstance(connected_to[0], int):
                connected_to = [{"target_id": i, "peso": 0, "tipo": "positiva"} for i in connected_to]

            nodo = NodeData(
                id=raw["id"],
                name=raw["name"],
                level=raw["level"],
                bribe_cost=raw["bribe_cost"],
                influence_gen=raw["influence_gen"],
                wealth_gen=raw["wealth_gen"],
                loyalty=raw["loyalty"],
                ambition=raw["ambition"],
                risk=raw["risk"],
                special_ability=raw["special_ability"],
                status=raw["status"],
                acepta_sobornos=raw["acepta_sobornos"],
                parent_id=raw["parent_id"],
                subordinados=raw["subordinados"],
                connected_to=connected_to,
                image_path=raw["image_path"],
                moral=raw.get("moral", 0)
            )
            nodos.append(nodo)

        return nodos

    def comprar(self):
        """
        Simula la compra de un nodo. Si el valor del soborno llega a cero,
        establece el nodo como comprado y realiza cambios en la estructura.
        """
        if self.bribe_cost <= 0:
            print(f"El nodo {self.name} ha sido comprado.")
            return True
        print(f"El nodo {self.name} no puede ser comprado, el soborno no ha llegado a cero.")
        return False

    def agregar_relacion(self, nodo_padre):
        """
        Establece una relación padre-hijo con otro nodo.
        """
        self.parent_id = nodo_padre.id
        self.subordinados.append(self.id)  # Agrega el nodo actual a la lista de subordinados del padre
        self.connected_to.append({"target_id": nodo_padre.id, "peso": 0, "tipo": "positiva"})  # Se agrega la conexión en el grafo
        print(f"Relación establecida: {nodo_padre.name} -> {self.name}")

    def guardar_en_json(self, path: str):
        """
        Guarda la instancia de este nodo en el archivo JSON, actualizando las relaciones.
        """
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        for node in raw_data:
            if node["id"] == self.id:
                node["parent_id"] = self.parent_id
                node["subordinados"] = self.subordinados
                node["connected_to"] = self.connected_to
                break

        with open(path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)
