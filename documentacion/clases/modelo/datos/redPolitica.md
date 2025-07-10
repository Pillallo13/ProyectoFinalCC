# redPolitica.json / redPoliticaCampana.json

Listas de nodos/personajes que conforman la red política del juego, con sus relaciones jerárquicas y de conexión.

**Estructura:**

```json
[
	{
		"id": 0,
		"name": "string",
		"level": "string",
		"bribe_cost": 0,
		"influence_gen": 0,
		"wealth_gen": 0,
		"loyalty": 0,
		"ambition": 0,
		"risk": 0,
		"special_ability": "string",
		"status": "string",
		"acepta_sobornos": true,
		"parent_id": 0,
		"subordinados": [0],
		"connected_to": [0],
		"image_path": "string"
	}
	// ...
]
```

**Campos:**

-   `id`: Identificador único del nodo/personaje.
-   `name`: Nombre del personaje.
-   `level`: Nivel jerárquico.
-   `bribe_cost`: Costo de soborno.
-   `influence_gen`: Influencia generada por turno.
-   `wealth_gen`: Riqueza generada por turno.
-   `loyalty`: Nivel de lealtad.
-   `ambition`: Nivel de ambición.
-   `risk`: Nivel de riesgo.
-   `special_ability`: Habilidad especial.
-   `status`: Estado actual.
-   `acepta_sobornos`: Si acepta sobornos.
-   `parent_id`: ID del nodo padre (o null si es raíz).
-   `subordinados`: Lista de IDs de subordinados.
-   `connected_to`: Lista de IDs de nodos conectados.
-   `image_path`: Ruta a la imagen del personaje.
