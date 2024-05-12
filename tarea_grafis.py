import heapq
import json
from collections import deque

import networkx as nx
from PyQt6.QtWidgets import QApplication
from matplotlib import pyplot as plt


class Red:
    def __init__(self, dirigida=False):
        self.dirigida = dirigida
        self.red = {}
        self.vertices = []

    def agregar_vertice(self, vertice):
        if vertice not in self.red:
            self.red[vertice] = {}
            self.vertices.append(vertice)
            self.vertices.sort()

    def agregar_arista(self, origen, destino, peso=1):
        if origen not in self.red:
            self.red[origen] = {}
        self.red[origen][destino] = peso

        if not self.dirigida:
            if destino not in self.red:
                self.red[destino] = {}
            self.red[destino][origen] = peso

    def eliminar_arista(self, origen, destino):
        if origen in self.red and destino in self.red[origen]:
            del self.red[origen][destino]
        else:
            print(f"No existe arista desde {origen} hacia {destino} para eliminar.")

        if not self.dirigida:
            if destino in self.red and origen in self.red[destino]:
                del self.red[destino][origen]
            else:
                print(f"No existe arista desde {destino} hacia {origen} para eliminar en una red no dirigida.")

    def dijkstra(self, inicio, destino=None):
        try:
            if inicio not in self.red:
                raise ValueError(f"El vértice de inicio '{inicio}' no existe en la red.")

            distancias = {vertice: float('inf') for vertice in self.vertices}
            distancias[inicio] = 0
            predecesores = {vertice: None for vertice in self.vertices}
            cola_prioridad = [(0, inicio)]
            visitados = set()

            while cola_prioridad:
                distancia_actual, vertice_actual = heapq.heappop(cola_prioridad)

                if vertice_actual in visitados:
                    continue
                visitados.add(vertice_actual)

                for vecino, peso in self.red[vertice_actual].items():
                    if vecino in visitados:
                        continue
                    nueva_distancia = distancia_actual + peso
                    if nueva_distancia < distancias[vecino]:
                        distancias[vecino] = nueva_distancia
                        predecesores[vecino] = vertice_actual
                        heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

                if vertice_actual == destino:
                    break

            if destino:
                if distancias[destino] == float('inf'):
                    return float('inf'), []
                else:
                    camino = []
                    paso = destino
                    while paso is not None:
                        camino.insert(0, paso)
                        paso = predecesores[paso]
                    return distancias[destino], camino
            return distancias, predecesores

        except Exception as e:
            print(f"Error en Dijkstra: {e}")
            raise

    def mostrar_matriz(self):
        matriz = [[0 for _ in self.vertices] for _ in self.vertices]
        print("Matriz de Adyacencia:")
        for i, origen in enumerate(self.vertices):
            for j, destino in enumerate(self.vertices):
                matriz[i][j] = self.red[origen].get(destino, 0)
            print(matriz[i])

    def dfs(self, inicio):
        visitados = set()
        orden = []

        def _dfs(vertice):
            if vertice not in visitados:
                visitados.add(vertice)
                orden.append(vertice)
                vecinos_ordenados = sorted(self.red.get(vertice, {}).keys())
                for vecino in vecinos_ordenados:
                    _dfs(vecino)

        _dfs(inicio)
        return orden

    def bfs(self, inicio):
        visitados = set([inicio])
        orden = []
        cola = deque([inicio])

        while cola:
            vertice = cola.popleft()
            orden.append(vertice)
            vecinos_ordenados = sorted(self.red.get(vertice, {}).keys())
            for vecino in vecinos_ordenados:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        return orden

    def es_simetrica(self):
        for i in self.vertices:
            for j in self.vertices:
                if self.red[i].get(j, 0) != self.red[j].get(i, 0):
                    return False
        return True

    def dibujar(self, ax, vertice_resaltado=None):
        ax.clear()
        G = nx.Graph()

        for vertice in self.vertices:
            G.add_node(vertice)

        for origen, destinos in self.red.items():
            for destino, peso in destinos.items():
                G.add_edge(origen, destino, weight=peso)

        pos = nx.spring_layout(G)  # Posicionamiento de los nodos usando el layout spring
        color_map = ['skyblue' if vertice != vertice_resaltado else 'red' for vertice in G.nodes()]
        nx.draw(G, pos, ax=ax, with_labels=True, node_color=color_map, edge_color='k', width=1.0, node_size=300)

        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_color='red')

        ax.figure.canvas.draw()
        QApplication.processEvents()  # Procesa los eventos de la GUI
        plt.pause(0.5)  # Una pausa breve para visualización

    def red_a_json(self):
        red_serializable = {'dirigida': self.dirigida, 'red': {}}
        for vertice, vecinos in self.red.items():
            red_serializable['red'][vertice] = {str(vecino): peso for vecino, peso in vecinos.items()}
        return red_serializable

    def guardar_red_en_json(self, nombre_archivo):
        red_serializable = self.red_a_json()
        with open(nombre_archivo, 'w') as archivo_json:
            json.dump(red_serializable, archivo_json, indent=4)

    def cargar_red_desde_json(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo_json:
            datos = json.load(archivo_json)

        self.dirigida = datos['dirigida']
        self.red = {}
        self.vertices = []

        for vertice, vecinos in datos['red'].items():
            self.agregar_vertice(vertice)
            for vecino, peso in vecinos.items():
                self.agregar_arista(vertice, vecino, peso)
