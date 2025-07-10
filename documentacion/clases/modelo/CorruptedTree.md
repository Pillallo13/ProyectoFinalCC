# CorruptedTree

Estructura de datos tipo árbol n-ario para modelar jerarquías corruptas.

Permite agregar personajes, establecer relaciones padre-hijo, consultar hijos, padres y atributos.
Incluye métodos para mostrar la estructura y cargar datos desde JSON.

**Atributos:**

-   `species_to_id` (dict): Mapea nombres a IDs únicos.
-   `id_to_species` (dict): Mapea IDs a nombres.
-   `parent_array` (list): Índices de padres por ID.
-   `children_map` (dict): Mapea IDs de padres a listas de hijos.
-   `attributes` (dict): Atributos completos de cada nodo/personaje.
-   `next_id` (int): Siguiente ID disponible.

**Métodos principales:**

-   `add_Person(name, parent_name=None, extra_attributes=None)`: Agrega un personaje y lo enlaza jerárquicamente.
-   `display_tree()`: Imprime la estructura del árbol.
-   `get_children(name)`: Devuelve los hijos de un personaje.
-   `get_parent(name)`: Devuelve el padre de un personaje.
-   `get_depth(name)`: Profundidad del personaje en el árbol.
-   `get_total_species()`: Total de nodos/personajes.
-   `get_attributes(name)`: Devuelve los atributos de un personaje.
-   `cargar_desde_json(json_data, tree)`: Carga nodos desde un JSON.
