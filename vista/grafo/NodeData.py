from dataclasses import dataclass
from vista.resources import IMAGES

@dataclass
class NodeData:
    id: int
    name: str
    level: str
    status: str
    loyalty: int
    ambition: int
    risk: int
    bribe_cost: int
    influence_gen: int
    wealth_gen: int
    special_ability: str
    image_path: str = (IMAGES["silhouette"])