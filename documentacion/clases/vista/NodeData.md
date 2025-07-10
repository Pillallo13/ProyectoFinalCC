# NodeData

Representa un nodo/personaje dentro de la red política del juego.

Modela la estructura jerárquica (árbol n-ario) y la red de conexiones (grafo).
Cada nodo puede tener un padre, subordinados y conexiones políticas.

**Atributos:**

-   `id` (int): Identificador único.
-   `name` (str): Nombre del personaje.
-   `level` (str): Nivel jerárquico.
-   `bribe_cost` (int): Costo de soborno.
-   `influence_gen` (int): Influencia generada por turno.
-   `wealth_gen` (int): Riqueza generada por turno.
-   `loyalty` (int): Nivel de lealtad (0-100).
-   `ambition` (int): Nivel de ambición (0-100).
-   `risk` (int): Nivel de riesgo (0-100).
-   `special_ability` (str): Habilidad especial.
-   `status` (str): Estado actual.
-   `acepta_sobornos` (bool): Si acepta sobornos.
-   `parent_id` (Optional[int]): ID del nodo padre.
-   `subordinados` (list[int]): IDs de subordinados.
-   `connected_to` (list[int]): IDs de nodos conectados.
-   `image_path` (str): Ruta de la imagen.
