from modelo.estructurasDeDatos.RedPolitica import RedPolitica

class GrafoController:
    def __init__(self, json_data):
        self.modelo = RedPolitica()
        self.modelo.cargar_desde_json(json_data)

    def agregar_relacion(self, origen, destino, tipo="desconocido", **datos):
        """Crea una relación en el grafo con atributos opcionales."""
        self.modelo.asociar(origen, destino, tipo=tipo, **datos)

    def obtener_relaciones_de(self, nodo_id):
        """Devuelve una lista de relaciones salientes desde un nodo."""
        return list(self.modelo.grafo.out_edges(nodo_id, data=True))

    def obtener_relaciones_hacia(self, nodo_id):
        """Devuelve una lista de relaciones entrantes hacia un nodo."""
        return list(self.modelo.grafo.in_edges(nodo_id, data=True))

    def obtener_todas_las_relaciones(self):
        """Lista completa de todas las relaciones del grafo."""
        return list(self.modelo.grafo.edges(data=True))

    def obtener_nodo(self, nodo_id):
        """Devuelve los atributos de un nodo por su ID."""
        return self.modelo.grafo.nodes[nodo_id]

    def visualizar(self, titulo="Grafo de relaciones corruptas"):
        """Muestra el grafo completo visualmente."""
        self.modelo.visualizar(titulo)

    def relaciones_por_tipo(self, tipo):
        """Devuelve todas las relaciones que sean de un tipo específico."""
        return [
            (u, v, d) for u, v, d in self.modelo.grafo.edges(data=True)
            if d.get("tipo") == tipo
        ]
