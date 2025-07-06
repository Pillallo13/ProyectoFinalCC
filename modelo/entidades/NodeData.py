import json
from dataclasses import dataclass, field
from typing import Optional
from vista.resources import IMAGES

@dataclass
class NodeData:
    """
    Representa un nodo/personaje dentro de la red política del juego.

    Esta clase modela tanto la estructura jerárquica (árbol n-ario) como la
    red de conexiones visuales (grafo). Cada nodo puede tener un padre, múltiples
    subordinados y relaciones políticas representadas por aristas.
    """

    """Identificador único del nodo."""
    id: int

    """Nombre del personaje político."""
    name: str

    """Nivel jerárquico del personaje (ej: Alcalde, Gobernador, Juez)."""
    level: str

    """Costo del soborno necesario para corromper a este personaje."""
    bribe_cost: int

    """Cantidad de puntos de influencia que genera por turno."""
    influence_gen: int

    """Cantidad de riqueza (dinero sucio) que genera por turno."""
    wealth_gen: int

    """Nivel de lealtad del personaje (0–100). Afecta resistencia o traición."""
    loyalty: int

    """Nivel de ambición (0–100). Afecta exigencias o intención de escalar."""
    ambition: int

    """Riesgo de exposición (0–100). Qué tan propenso es a ser descubierto."""
    risk: int

    """Habilidad especial que distingue al personaje (ej: Compra de votos)."""
    special_ability: str

    """Estado actual del personaje (ej: Activo, Investigado, Quemado, etc.)."""
    status: str

    """Indica si actualmente acepta sobornos. Puede cambiar durante la partida."""
    acepta_sobornos: bool

    """ID del nodo padre en el árbol jerárquico. None si es nodo raíz."""
    parent_id: Optional[int] = None

    """Lista de IDs de subordinados (estructura n-aria)."""
    subordinados: list[int] = field(default_factory=list)

    """Lista de IDs de nodos conectados en la vista de grafo."""
    connected_to: list[int] = field(default_factory=list)

    """Ruta a la imagen del personaje (para visualización en la interfaz)."""
    image_path: str = IMAGES["silhouette"]

    @staticmethod
    def cargar_desde_json(path: str) -> list["NodeData"]:
        """
        Carga una lista de nodos desde un archivo JSON.

        Args:
            path (str): Ruta al archivo JSON.

        Returns:
            list[NodeData]: Lista de nodos construidos desde el archivo.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [NodeData(**n) for n in data]
