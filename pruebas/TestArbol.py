import json
from modelo.estructurasDeDatos.CorruptedTree import CorruptedTree, cargar_desde_json

if __name__ == "__main__":
    # Ruta al JSON expandido con varios niveles de hijos y nietos
    ruta = "../modelo/datos/redPoliticaCampana.json"

    # Cargar datos desde el archivo
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Crear el árbol y cargar los datos
    tree = CorruptedTree()
    cargar_desde_json(data, tree)

    # Mostrar el árbol completo
    print("=== ARBOL DE PODER CORRUPTO ===")
    tree.display_tree()

    # Verificar atributos por ID
    print("\n=== ATRIBUTOS DEL NODO ID 6 (Abogado Sibilino) ===")
    print(tree.get_attributes_by_json_id(6))

    print("\n=== ATRIBUTOS DEL NODO ID 13 (Inspector Mañoso) ===")
    print(tree.get_attributes_by_json_id(13))

    # Obtener hijos directos del alcalde (id: 1)
    alcalde_id = 1
    alcalde_species_id = tree.json_id_to_species_id.get(alcalde_id)
    hijos = tree.children_map.get(alcalde_species_id, [])
    nombres_hijos = [tree.id_to_species[hid] for hid in hijos]
    print(f"\n=== HIJOS DIRECTOS DE ALCALDE (ID 1) ===\n{nombres_hijos}")

    # Profundidad de Inspector Mañoso
    nombre_inspector = tree.id_to_species[tree.json_id_to_species_id[13]]
    profundidad = tree.get_depth(nombre_inspector)
    print(f"\n=== PROFUNDIDAD DEL INSPECTOR MAÑOSO ===\n{profundidad}")
