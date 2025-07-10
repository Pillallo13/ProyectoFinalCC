from controlador.campanna.NodoController import NodoController, comprar_y_relacionar

# Ruta al archivo JSON
path_json = "../modelo/datos/infinito/redPolitica.json"

# Cargar los nodos usando el controlador
controlador = NodoController(path_json)

# Obtener los nodos (supongamos que nodo1 compra nodo2)
nodo_comprador = controlador.buscar_por_id(1)  # Nodo 1 (padre)
nodo_comprado = controlador.buscar_por_id(2)  # Nodo 2 (hijo)

# Realizamos la compra y establecemos la relación
comprar_y_relacionar(nodo_comprador, nodo_comprado, path_json)

# Comprobar si los datos en el archivo JSON fueron actualizados correctamente
# Vuelve a cargar los nodos después de la compra
nodos_actualizados = controlador.obtener_todos()
for nodo in nodos_actualizados:
    print(f"{nodo.name} - Parent ID: {nodo.parent_id} - Subordinados: {nodo.subordinados}")
