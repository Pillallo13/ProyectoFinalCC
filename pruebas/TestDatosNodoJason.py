import os
import json
from modelo.entidades.NodeData import NodeData

# Calcula la ruta del archivo JSON en función de la ubicación de este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.normpath(os.path.join(BASE_DIR,"../modelo/datos/redPolitica.json"))

def cargar_nodos(path=JSON_PATH) -> list[NodeData]:
    """Carga los nodos desde el archivo JSON."""
    print(f" Cargando JSON desde: {os.path.abspath(path)}")

    if not os.path.exists(path):
        print(" Archivo no encontrado en la ruta especificada.")
        exit(1)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [NodeData(**n) for n in data]

def buscar_nodo_por_id(nodos: list[NodeData], id_buscado: int) -> NodeData | None:
    """Busca un nodo por su ID en la lista de nodos."""
    for nodo in nodos:
        if nodo.id == id_buscado:
            return nodo
    return None

def imprimir_nodo(nodo: NodeData):
    """Muestra todos los datos del nodo en consola de forma legible."""
    print("\n Datos del Nodo:")
    print(f"ID: {nodo.id}")
    print(f"Nombre: {nodo.name}")
    print(f"Nivel: {nodo.level}")
    print(f"Estado: {nodo.status}")
    print(f"Acepta sobornos: {'Sí' if nodo.acepta_sobornos else 'No'}")
    print(f"Lealtad: {nodo.loyalty}")
    print(f"Ambición: {nodo.ambition}")
    print(f"Riesgo: {nodo.risk}")
    print(f"Costo Soborno: ${nodo.bribe_cost:,}")
    print(f"Influencia/turno: {nodo.influence_gen}")
    print(f"Riqueza/turno: ${nodo.wealth_gen:,}")
    print(f"Habilidad especial: {nodo.special_ability}")
    print(f"Padre: {nodo.parent_id}")
    print(f"Subordinados: {nodo.subordinados}")
    print(f"Conectado con: {nodo.connected_to}")
    print(f"Imagen: {nodo.image_path}")
    print()

if __name__ == "__main__":
    nodos = cargar_nodos()
    try:
        id_deseado = int(input("🔍 Ingrese el ID del nodo a consultar: "))
    except ValueError:
        print(" Entrada inválida. Debe ser un número entero.")
        exit(1)

    nodo = buscar_nodo_por_id(nodos, id_deseado)

    if nodo:
        imprimir_nodo(nodo)
    else:
        print(" Nodo no encontrado.")
