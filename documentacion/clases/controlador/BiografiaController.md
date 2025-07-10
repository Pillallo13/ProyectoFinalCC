# BiografiaController

Controlador para la gestión de biografías de personajes históricos o políticos.

Carga los datos de un personaje y sus eventos biográficos desde un archivo JSON, permitiendo acceder a la información y buscar eventos específicos por ID.

**Atributos:**

-   `path_json` (str): Ruta al archivo JSON de biografía.
-   `_personaje` (PersonajeData): Instancia con los datos del personaje.
-   `_eventos` (list[EventosData]): Lista de eventos biográficos.

**Métodos principales:**

-   `get_personaje()`: Devuelve el personaje cargado.
-   `buscar_evento_por_id(id_evento)`: Busca y retorna un evento por su ID.
