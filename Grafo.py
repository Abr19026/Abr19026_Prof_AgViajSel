from typing import (Any, FrozenSet, Tuple, NamedTuple, Iterable )

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from heapq import *

#Archivo con las definiciones de la clase grafo

tipo_nodo = str

class Arista:
    
    def __init__(self, vecinos: Tuple[tipo_nodo, tipo_nodo], peso: float=0):
        if len(vecinos) != 2:
            raise Exception("Arista no valida")
        self.vecinos: tuple[tipo_nodo, tipo_nodo] = vecinos
        self.peso = peso

    def __repr__(self):
        nodos_string = ", ".join(map(str, self.vecinos))
        return f"( {nodos_string} :: {self.peso} )"

    def __eq__(self, o):
        return isinstance(o, Arista) \
            and frozenset(self.vecinos) == frozenset(o.vecinos) \
            and self.peso == o.peso

    def __hash__(self):
        return hash(frozenset(self.vecinos))

    def __iter__(self):
        return iter(self.vecinos)

    def arista_nx(self)-> Tuple[tipo_nodo, tipo_nodo, dict]:
        return (self.vecinos[0], self.vecinos[1], {"weight": self.peso})

# Función para agregar valores a diccionario aunque no exista
def aumentar_dict_dict(diccionario: dict[tipo_nodo, dict[tipo_nodo, float]], nodo1, nodo2, peso):
    if nodo1 in diccionario:
        diccionario[nodo1][nodo2] = peso
    else:
        diccionario[nodo1] = {nodo2: peso}

class Grafo:
    def __init__(self, adyacencias: Iterable[Arista], valoresnodos: dict[tipo_nodo, float]):
        self.adyacencias: dict[tipo_nodo, dict[tipo_nodo,float]] = {}
        self.valor_nodo: dict[tipo_nodo, float] = valoresnodos;
        for arista in adyacencias:
            self.agregar_arista(arista)

    def __str__(self):
        salida = ""
        for nodo in self.adyacencias.keys():
            salida += f"{nodo}: {self.adyacencias[nodo]}\n"
        return salida

    # Limitante: Solo puede haber 1 arista entre cada par de nodos
    def agregar_arista(self, arista: Arista):
        for i, nodo in enumerate(arista.vecinos):
            nodo_vecino = arista.vecinos[1 - i]
            aumentar_dict_dict(self.adyacencias, nodo, nodo_vecino, arista.peso)

    # Elimina la arista con el par de vecinos dados sin importar el peso
    def eliminar_arista(self, arista: Arista):
        for i, nodo in enumerate(arista.vecinos):
            nodo_vecino = arista.vecinos[1 - i]
            del self.adyacencias[nodo][nodo_vecino]
            if nodo_vecino == nodo:
                break

    def get_nodos(self):
        return self.adyacencias.keys()

    def get_vecinos(self, nodo: tipo_nodo) -> FrozenSet[tipo_nodo]:
        return frozenset(self.adyacencias[nodo].keys())

    def get_aristas(self) -> FrozenSet[Arista]:
        set_aristas: set[Arista] = set()
        for nodo in self.get_nodos():
            for vecino in self.get_vecinos(nodo):
                set_aristas.add(Arista((nodo, vecino), self.adyacencias[nodo][vecino]))
        return frozenset(set_aristas)

    def costo_arista(self, nodo1:tipo_nodo, nodo2: tipo_nodo) -> float:
        return self.adyacencias[nodo1][nodo2]

    def graficar(self):
        # Convierte grafo a networkx
        grafo_nx = nx.Graph()
        grafo_nx.add_edges_from([arista.arista_nx() for arista in self.get_aristas()])

        for nodo, valor in self.valor_nodo.items():
            grafo_nx.nodes[nodo]["weight"] = valor

        # Grafica grafo
        pos=nx.spring_layout(grafo_nx)
        nx.draw_networkx(grafo_nx, pos)
        edge_labels = nx.get_edge_attributes(grafo_nx,'weight')
        node_states = nx.get_node_attributes(grafo_nx, 'weight')
        state_pos = {n: (x+0.12, y+0.05) for n, (x,y) in pos.items()}

        nx.draw_networkx_labels(grafo_nx, state_pos, labels=node_states, font_color='red')
        nx.draw_networkx_edge_labels(grafo_nx, pos, edge_labels=edge_labels);

        plt.show()

    def dijkstra(self, origen) -> dict[tipo_nodo, tuple[float, tipo_nodo]]:
        """Implementación del algoritmo de Dijkstra para encontrar las distancias más cortas desde un nodo origen a todos los demás nodos en el grafo."""
        distancias = {v: (float('inf'),None) for v in self.get_nodos()}
        distancias[origen] = (0,None)
        heap = [(0, origen)]
        while heap:
            (dist, v) = heap.heappop(heap)
            if dist > distancias[v][0]:
                continue
            for w in self.get_vecinos(v):
                distancia_nueva = dist + self.adyacencias[v][w]
                if distancia_nueva < distancias[w][0]:
                    distancias[w] = (distancia_nueva,v)
                    heap.heappush(heap, (distancia_nueva, w))
        return distancias
