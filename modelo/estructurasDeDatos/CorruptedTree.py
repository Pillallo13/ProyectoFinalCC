class CorruptedTree:
    def __init__(self):
        self.species_to_id = {}
        self.id_to_species = {}
        self.parent_array = []
        self.children_map = {}
        self.attributes = {}  # Guarda los atributos completos del nodo
        self.next_id = 0

    def add_Person(self, name, parent_name=None, extra_attributes=None):
        if name not in self.species_to_id:
            species_id = self.next_id
            self.species_to_id[name] = species_id
            self.id_to_species[species_id] = name
            self.next_id += 1

            while len(self.parent_array) <= species_id:
                self.parent_array.append(None)

            if parent_name and parent_name in self.species_to_id:
                parent_id = self.species_to_id[parent_name]
                self.parent_array[species_id] = parent_id
                if parent_id not in self.children_map:
                    self.children_map[parent_id] = []
                self.children_map[parent_id].append(species_id)
            else:
                self.parent_array[species_id] = -1

            # Guardar atributos
            if extra_attributes:
                self.attributes[species_id] = extra_attributes
            else:
                self.attributes[species_id] = {}
        else:
            species_id = self.species_to_id[name]
            if parent_name and parent_name in self.species_to_id:
                parent_id = self.species_to_id[parent_name]
                self.parent_array[species_id] = parent_id
                if parent_id not in self.children_map:
                    self.children_map[parent_id] = []
                if species_id not in self.children_map[parent_id]:
                    self.children_map[parent_id].append(species_id)
            if extra_attributes:
                self.attributes[species_id] = extra_attributes

        return self.species_to_id[name]

    def display_tree(self):
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
        parent_id = self.species_to_id.get(name)
        if parent_id is None:
            return []
        return [self.id_to_species[child_id] for child_id in self.children_map.get(parent_id, [])]

    def get_parent(self, name):
        species_id = self.species_to_id.get(name)
        if species_id is None:
            return None
        parent_id = self.parent_array[species_id]
        return self.id_to_species.get(parent_id, None) if parent_id != -1 else None

    def get_depth(self, name):
        species_id = self.species_to_id.get(name)
        depth = 0
        while species_id is not None and self.parent_array[species_id] != -1:
            species_id = self.parent_array[species_id]
            depth += 1
        return depth

    def get_total_species(self):
        return self.next_id

    def get_attributes(self, name):
        species_id = self.species_to_id.get(name)
        return self.attributes.get(species_id, {}) if species_id is not None else None


def cargar_desde_json(json_data, tree: CorruptedTree):
    id_a_nombre = {entry["id"]: entry["name"] for entry in json_data}

    for entry in json_data:
        name = entry["name"]
        parent_id = entry["parent_id"]
        parent_name = id_a_nombre.get(parent_id) if parent_id is not None else None
        tree.add_Person(name, parent_name, entry)
