# NodoController

Controlador para la gestión de nodos de la red política.

Carga los nodos desde un archivo JSON y permite buscarlos por ID o recuperar todos.

**Atributos:**

-   `path_json` (str): Ruta al archivo JSON de nodos.
-   `nodos` (list[NodeData]): Lista de nodos cargados.
