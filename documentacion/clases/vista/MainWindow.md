# MainWindow

Ventana principal de la aplicación.

Gestiona la navegación entre las diferentes vistas del juego usando un QStackedWidget.
Permite cambiar entre menú principal, selección de modo, juego principal y pantalla de derrota.

**Atributos:**

-   `player_name` (str): Nombre del jugador.
-   `stacked_widget` (QStackedWidget): Contenedor de vistas.
-   `main_menu` (MainMenu): Vista del menú principal.
-   `game_mode_selection` (GameModeSelection): Pantalla de selección de modo.
-   `main_game_ui` (MainGameHistoriaUI): Vista principal del juego.
-   `defeat_screen` (DefeatScreen): Pantalla de derrota.
