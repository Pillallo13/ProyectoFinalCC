
## Estructura del archivo `redPolitica.json` – **Documentación de campos**

Cada elemento del array representa un **personaje de la red política**. Cada personaje contiene:

### 🔑 Atributos por nodo

|Campo|Tipo|Descripción|
|---|---|---|
|`id`|`int`|Identificador único del nodo/personaje. Requerido para construir el grafo y la jerarquía del árbol.|
|`name`|`str`|Nombre del personaje político.|
|`level`|`str`|Nivel jerárquico dentro de la red (ej.: Alcalde, Concejal, Juez).|
|`bribe_cost`|`int`|Cantidad de dinero necesaria para sobornarlo. Afecta decisiones del jugador.|
|`influence_gen`|`int`|Puntos de influencia que genera por turno. Se acumulan en el HUD.|
|`wealth_gen`|`int`|Dinero sucio que genera por turno.|
|`loyalty`|`int` (0-100)|Nivel de lealtad. A mayor valor, menor probabilidad de traición o filtración.|
|`ambition`|`int` (0-100)|Nivel de ambición personal. A mayor valor, mayor probabilidad de intentar escalar, desobedecer o traicionar.|
|`risk`|`int` (0-100)|Nivel de riesgo de ser descubierto o cometer errores. Afecta exposición.|
|`special_ability`|`str`|Habilidad especial del personaje. Ej.: "Compra de Votos", "Contratación Amañada", etc.|
|`status`|`str`|Estado actual del personaje: `"Activo"`, `"Bajo Sospecha"`, `"Investigado"`, `"Quemado"`, `"Encarcelado"` u otros.|
|`acepta_sobornos`|`bool`|Si acepta sobornos inicialmente. Puede cambiar por eventos o manipulación del jugador.|
|`parent_id`|`int|null`|
|`subordinados`|`list[int]`|Lista de IDs de nodos hijos en el árbol jerárquico. Representa los contactos directos bajo su control.|
|`connected_to`|`list[int]`|Lista de IDs de nodos conectados visualmente en el grafo. Puede incluir subordinados, aliados, u otros vínculos.|
|`image_path`|`str`|Ruta relativa a la imagen del personaje. Usada en la vista gráfica (`GraphNodeItem`, `ContactDetailDialog`, etc).|

---

###  Notas adicionales

- La **estructura de árbol n-ario** se construye con `parent_id` y `subordinados`.
    
- Las conexiones del **grafo visual** se definen con `connected_to`, que puede o no coincidir con la jerarquía.
    
- Este JSON puede crecer libremente con más personajes mientras se respeten estos campos.
    