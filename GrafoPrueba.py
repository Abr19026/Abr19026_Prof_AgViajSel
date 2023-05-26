from Grafo import Arista, Grafo
adyacencias = [
    Arista(("A","B"),6),
    Arista(("A","C"),8),
    Arista(("A","D"),5),
    Arista(("B","C"),4),
    Arista(("B","D"),7),
    Arista(("C","D"),5)
]

valores_nodos = {
    "A": 0,
    "B": 5,
    "C": 2,
    "D": 3
}

if __name__ == "__main__":
    migrafo = Grafo(adyacencias, valores_nodos)
    migrafo.graficar()