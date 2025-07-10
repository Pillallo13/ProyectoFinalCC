class CorruptedTree:
    """
    Representa una estructura jerárquica (árbol) construida a partir de datos JSON.
    Cada nodo es identificado por un ID del JSON ("json_id"), pero internamente se
    usa un índice continuo ("species_id") para facilitar el manejo de listas y recorridos.
    """

    def __init__(self):
        # Mapeo de nombre a species_id (usado en funciones basadas en nombre; puede eliminarse si se usa solo json_id)
        self.species_to_id = {}

        # Mapeo de species_id a nombre (usado para mostrar nombres en display_tree)
        self.id_to_species = {}

        # Arreglo que guarda el species_id del padre de cada nodo
        self.parent_array = []

        # Diccionario que guarda los hijos de cada species_id
        self.children_map = {}

        # Diccionario que guarda los atributos completos de cada nodo, indexados por species_id
        self.attributes = {}

        # Mapeo directo del id del JSON (json_id) al species_id interno del árbol
        self.json_id_to_species_id = {}

        # Contador interno para asignar species_id consecutivos
        self.next_id = 1

    def add_person(self, name, parent_name=None, extra_attributes=None):
        """
        Añade un nodo al árbol. Si el nombre ya existe, actualiza su padre y atributos si se proveen.
        Usa el campo 'id' dentro de extra_attributes para mapear json_id → species_id.
        """
        if name not in self.species_to_id:
            # Asignar nuevo species_id
            species_id = self.next_id
            self.species_to_id[name] = species_id
            self.id_to_species[species_id] = name
            self.next_id += 1

            # Registrar mapeo json_id → species_id si se provee
            if extra_attributes and "id" in extra_attributes:
                self.json_id_to_species_id[extra_attributes["id"]] = species_id

            # Asegurar que el arreglo de padres tenga suficiente longitud
            while len(self.parent_array) <= species_id:
                self.parent_array.append(None)

            # Establecer relación padre-hijo si el padre existe
            if parent_name and parent_name in self.species_to_id:
                parent_id = self.species_to_id[parent_name]
                self.parent_array[species_id] = parent_id
                self.children_map.setdefault(parent_id, []).append(species_id)
            else:
                # Nodo raíz
                self.parent_array[species_id] = -1

            # Guardar atributos del nodo
            self.attributes[species_id] = extra_attributes or {}

        else:
            # Nodo ya existe, solo actualizar si se proporcionan nuevos datos
            species_id = self.species_to_id[name]
            if parent_name and parent_name in self.species_to_id:
                parent_id = self.species_to_id[parent_name]
                self.parent_array[species_id] = parent_id
                self.children_map.setdefault(parent_id, [])
                if species_id not in self.children_map[parent_id]:
                    self.children_map[parent_id].append(species_id)

            if extra_attributes:
                self.attributes[species_id] = extra_attributes
                if "id" in extra_attributes:
                    self.json_id_to_species_id[extra_attributes["id"]] = species_id

    def display_tree(self):
        """
        Imprime el árbol jerárquico completo de forma indentada, comenzando desde la raíz.
        Muestra nombre, nivel, estado y species_id.
        """

        def _display_recursive(species_id, level=0):
            indent = "    " * level
            name = self.id_to_species[species_id]
            node_info = self.attributes.get(species_id, {})
            nivel = node_info.get("level", "Desconocido")
            estado = node_info.get("status", "Desconocido")
            print(f"{indent}- {name} (Nivel: {nivel}, Estado: {estado}, ID: {species_id})")

            for child_id in self.children_map.get(species_id, []):
                _display_recursive(child_id, level + 1)

        root_ids = [sid for sid, pid in enumerate(self.parent_array) if pid == -1]
        for root_id in root_ids:
            _display_recursive(root_id)

    def get_children(self, name):
        """
        Retorna una lista con los nombres de los hijos del nodo dado.
        (Función auxiliar basada en nombre, puede omitirse si se trabaja solo con IDs)
        """
        parent_id = self.species_to_id.get(name)
        if parent_id is None:
            return []
        return [self.id_to_species[child_id] for child_id in self.children_map.get(parent_id, [])]

    def get_parent(self, name):
        """
        Retorna el nombre del padre del nodo dado.
        (Función auxiliar basada en nombre, puede omitirse si se trabaja solo con IDs)
        """
        species_id = self.species_to_id.get(name)
        if species_id is None:
            return None
        parent_id = self.parent_array[species_id]
        return self.id_to_species.get(parent_id, None) if parent_id != -1 else None

    def get_depth(self, name):
        """
        Retorna la profundidad del nodo con respecto a la raíz.
        (Función auxiliar basada en nombre, puede omitirse si se trabaja solo con IDs)
        """
        species_id = self.species_to_id.get(name)
        depth = 0
        while species_id is not None and self.parent_array[species_id] != -1:
            species_id = self.parent_array[species_id]
            depth += 1
        return depth

    def get_total_species(self):
        """
        Retorna la cantidad total de nodos insertados.
        """
        return self.next_id

    def get_attributes_by_json_id(self, json_id):
        """
        Retorna los atributos completos del nodo identificado por el ID original del JSON.
        """
        species_id = self.json_id_to_species_id.get(json_id)
        return self.attributes.get(species_id, {}) if species_id is not None else None


def cargar_desde_json(json_data, tree: CorruptedTree):
    """
    Carga los nodos desde un arreglo JSON. Establece relaciones jerárquicas padre-hijo
    y registra atributos completos de cada entrada. Usa el campo 'parent_id' para enlazar jerarquías.
    """
    # Crear un mapa auxiliar: json_id → name (para traducir parent_id a nombre)
    id_a_nombre = {entry["id"]: entry["name"] for entry in json_data}

    for entry in json_data:
        name = entry["name"]
        parent_id = entry.get("parent_id")
        parent_name = id_a_nombre.get(parent_id) if parent_id is not None else None
        tree.add_person(name, parent_name, entry)
