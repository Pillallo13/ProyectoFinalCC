from modelo.estructurasDeDatos.CorruptedTree import CorruptedTree, cargar_desde_json

class ArbolController:
    def __init__(self, json_data):
        self.arbol = CorruptedTree()
        cargar_desde_json(json_data, self.arbol)

    def agregar_persona(self, name, parent_name=None, atributos=None):
        return self.arbol.add_person(name, parent_name, atributos)

    def obtener_hijos(self, nombre):
        return self.arbol.get_children(nombre)

    def obtener_padre(self, nombre):
        return self.arbol.get_parent(nombre)

    def obtener_profundidad(self, nombre):
        return self.arbol.get_depth(nombre)

    def obtener_atributos(self, json_id):
        return self.arbol.get_attributes_by_json_id(json_id)

    def mostrar_arbol(self):
        self.arbol.display_tree()

    def total_nodos(self):
        return self.arbol.get_total_species()
