# partidas_guardadas.json

Lista de partidas guardadas, cada una representando el estado de un personaje/nodo en la red política.

**Estructura:**

```json
[
	{
		"id": 0,
		"name": "string",
		"level": "string",
		"status": "string",
		"loyalty": 0,
		"ambition": 0,
		"risk": 0,
		"bribe_cost": 0,
		"influence_gen": 0,
		"wealth_gen": 0,
		"special_ability": "string",
		"parent_id": 0,
		"connected_to": [0]
	}
	// ...
]
```

**Campos:**

-   `id`: Identificador único del nodo/personaje.
-   `name`: Nombre del personaje.
-   `level`: Nivel jerárquico.
-   `status`: Estado actual.
-   `loyalty`: Nivel de lealtad.
-   `ambition`: Nivel de ambición.
-   `risk`: Nivel de riesgo.
-   `bribe_cost`: Costo de soborno.
-   `influence_gen`: Influencia generada por turno.
-   `wealth_gen`: Riqueza generada por turno.
-   `special_ability`: Habilidad especial.
-   `parent_id`: ID del nodo padre (o null si es raíz).
-   `connected_to`: Lista de IDs de nodos conectados.
