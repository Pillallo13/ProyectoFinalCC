# biografia.json

Contiene la biografía de un personaje histórico o político y una lista de eventos relevantes de su vida.

**Estructura:**

```json
{
	"personaje": {
		"nombre_completo": "string",
		"fecha_nacimiento": "string",
		"lugar_nacimiento": "string",
		"profesion": "string"
	},
	"relato": [
		{
			"id_evento": "string",
			"texto": "string"
		}
		// ...
	]
}
```

**Campos:**

-   `personaje`: Objeto con los datos principales del personaje.
    -   `nombre_completo`: Nombre completo del personaje.
    -   `fecha_nacimiento`: Fecha de nacimiento.
    -   `lugar_nacimiento`: Lugar de nacimiento.
    -   `profesion`: Profesión principal.
-   `relato`: Lista de eventos biográficos.
    -   `id_evento`: Identificador único del evento.
    -   `texto`: Descripción del evento.
