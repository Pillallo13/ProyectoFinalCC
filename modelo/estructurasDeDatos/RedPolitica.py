import networkx as nx
import matplotlib.pyplot as plt

class RedPolitica:
    def __init__(self):
        self.grafo = nx.DiGraph()

    def agregar_nodo(self, id, nombre, **atributos):
        """Agrega un nodo con atributos específicos."""
        self.grafo.add_node(id, label=nombre, **atributos)

    def asociar(self, origen_id, destino_id, tipo="desconocido", peso=1, **atributos_extra):
        """Crea una relación entre dos nodos con tipo y peso."""
        self.grafo.add_edge(origen_id, destino_id, tipo=tipo, peso=peso, **atributos_extra)

    def activar_investigacion(self, nodo_id, tipo="investigacion"):
        """
        Activa una investigación en el nodo dado (si está conectado a un fiscal incorruptible).
        La investigación se propaga en el grafo.
        """
        # Si el nodo está conectado a un fiscal incorruptible, se activa la investigación
        for vecino in self.grafo.neighbors(nodo_id):
            if self.grafo.nodes[vecino].get("label") == "Fiscal Incorruptible":
                print(f"Investigación iniciada en {nodo_id} debido a una acción riesgosa.")
                self.asociar(nodo_id, vecino, tipo="investigacion", peso=-10)  # Relación negativa (investigación)
                return True
        return False

    def visualizar(self, titulo="Red Política Corrupta"):
        pos = nx.spring_layout(self.grafo, k=0.7)
        edge_types = nx.get_edge_attributes(self.grafo, 'tipo')
        edge_weights = nx.get_edge_attributes(self.grafo, 'peso')

        plt.figure(figsize=(14, 10))
        nx.draw_networkx_nodes(self.grafo, pos, node_size=1000, node_color='lightgray')
        nx.draw_networkx_labels(self.grafo, pos, labels=nx.get_node_attributes(self.grafo, 'label'), font_size=9)

        # Dibujar aristas con peso
        for tipo in set(edge_types.values()):
            edges = [(u, v) for u, v, d in self.grafo.edges(data=True) if d['tipo'] == tipo]
            nx.draw_networkx_edges(self.grafo, pos, edgelist=edges, width=2, arrows=True)

        # Dibujar las aristas con peso
        for u, v, d in self.grafo.edges(data=True):
            peso = d.get('peso', 1)
            nx.draw_networkx_edges(self.grafo, pos, edgelist=[(u, v)], width=peso * 0.5, edge_color='black')

        plt.title(titulo)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
