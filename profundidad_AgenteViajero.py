from Grafo import Grafo, tipo_nodo
from GrafoPrueba import adyacencias, valores_nodos

nodo_inicial = "A"
grafo = Grafo(adyacencias,valores_nodos)
ruta_corta = grafo.dijkstra(nodo_inicial)
distancia_maxima = 1000

nodos_restantes = set(grafo.get_nodos())
camino_actual = [nodo_inicial]
peso_camino_actual = 0
valor_camino_actual = 0

mejor_camino = None
peso_mejor_camino = float("inf")
valor_mejor_camino = 0

def agregar_nodo_camino(nodo):
    if nodo not in camino_actual:
        valor_mejor_camino += grafo.valor_nodo[nodo]
    peso_camino_actual += grafo.costo_arista(camino_actual[-1],nodo)
    camino_actual.append(nodo)

def quitar_nodo_camino():
    quitado = camino_actual.pop()
    peso_camino_actual -= grafo.costo_arista(camino_actual[-1], quitado)
    if quitado not in camino_actual:
        valor_mejor_camino -= grafo.valor_nodo[quitado]

# solo funciona con NO Dirigidos
def profundidad_viajero_selectivo(nodo_actual: tipo_nodo):
    for nodo_vecino in  grafo.get_vecinos(nodo_actual):
        agregar_nodo_camino(nodo_vecino)
        # Si aún es posible un camino valido
        if (peso_camino_actual + ruta_corta[nodo_vecino][0]) <= distancia_maxima:
            # Si el camino es factible
            if nodo_vecino == nodo_inicial and peso_camino_actual < peso_mejor_camino:
                mejor_camino = camino_actual.copy()
                peso_mejor_camino = peso_camino_actual
            # Halla posibles caminos del hijo
            profundidad_viajero_selectivo(nodo_vecino)
        quitar_nodo_camino()
    return

print(f"distancia del mejor camino: {peso_mejor_camino}")
print(mejor_camino)