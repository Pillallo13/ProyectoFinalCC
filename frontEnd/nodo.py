from dataclasses import dataclass, field

@dataclass
class NodeData:
    id: int
    name: str
    level: str
    status: str  # 'Activo', 'Bajo Sospecha', 'Investigado', 'Quemado'
    loyalty: int
    ambition: int
    risk: int
    bribe_cost: int
    influence_gen: int
    wealth_gen: int
    special_ability: str
    image_path: str = "frontEnd/images/silhouette.png"