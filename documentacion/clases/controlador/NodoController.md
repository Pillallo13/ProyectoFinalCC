# NodoController

Controlador para la gestión de nodos de la red política.

Carga los nodos desde un archivo JSON y permite buscarlos por ID o recuperar todos.

**Atributos:**

-   `path_json` (str): Ruta al archivo JSON de nodos.
-   `nodos` (list[NodeData]): Lista de nodos cargados.

**Métodos principales:**

-   `buscar_por_id(nodo_id)`: Busca y retorna un nodo por su ID.
-   `obtener_todos()`: Devuelve la lista de todos
