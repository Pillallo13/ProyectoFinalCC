import json

from modelo.estructurasDeDatos.CorruptedTree import CorruptedTree, cargar_desde_json

if __name__ == "__main__":
    with open("../modelo/datos/redPoliticaCampana.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tree = CorruptedTree()
    cargar_desde_json(data, tree)

    print("=== ARBOL DE PODER CORRUPTO ===")
    tree.display_tree()

    print("\n=== ATRIBUTOS DE 'Concejal Tuerquilla' ===")
    print(tree.get_attributes("Concejal Tuerquilla"))
