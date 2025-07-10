# MainGameHistoriaUI

Vista principal del juego en modo campaña.

Contiene el área del grafo, HUD con estadísticas y botón de finalizar turno.
Permite consultar detalles de cada contacto corrupto.

**Atributos:**

-   `switch_to_defeat` (callable): Cambia a pantalla de derrota.
-   `controller` (NodoController): Acceso a los datos de nodos.
-   `player_name_label` (QLabel): Nombre del jugador.
-   `capital_label` (QLabel): Capital político.
-   `money_label` (QLabel): Dinero sucio.
-   `influence_label` (QLabel): Influencia.
-   `suspicion_bar` (QProgressBar): Nivel de sospecha.
