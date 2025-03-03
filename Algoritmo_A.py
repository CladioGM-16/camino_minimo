import heapq
import math
from Grafo_Dijkstra import posicion


def heuristica(a, b):
    """Función heurística para A* basada en la distancia euclidiana."""
    (x1, y1) = posicion[a]
    (x2, y2) = posicion[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def a_estrella(grafo, inicio, fin):
    cola = [(0, inicio, [])]
    visitados = set()
    coste_acumulado = {inicio: 0}

    while cola:
        (coste, nodo, camino) = heapq.heappop(cola)

        if nodo in visitados:
            continue

        camino = camino + [nodo]
        visitados.add(nodo)

        if nodo == fin:
            return coste_acumulado[nodo], camino

        for (vecino, peso) in grafo.get(nodo, []):
            if vecino not in visitados:
                nuevo_coste = coste_acumulado[nodo] + peso
                if vecino not in coste_acumulado or nuevo_coste < coste_acumulado[vecino]:
                    coste_acumulado[vecino] = nuevo_coste
                    prioridad = nuevo_coste + heuristica(vecino, fin)
                    heapq.heappush(cola, (prioridad, vecino, camino))

    return float("inf"), []
