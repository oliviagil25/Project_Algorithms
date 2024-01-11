import pandas as pd
import sys

def nearest_neighbor(graph, start):
    num_vertices = len(graph)
    visited = [False] * num_vertices
    path = [start]
    visited[start] = True
    distance = 0

    for i in range(num_vertices - 1):
        min_weight = sys.maxsize
        next_vertex = -1
        current_vertex = path[-1]
        for neighbor in range(num_vertices):
            if not visited[neighbor] and graph.iloc[current_vertex, neighbor] < min_weight:
                min_weight = graph.iloc[current_vertex, neighbor]
                next_vertex = neighbor

        if next_vertex != -1:
            path.append(next_vertex)
            visited[next_vertex] = True
            distance += min_weight

    distance += graph.iloc[path[-1], start]

    return path, distance

def best_path(graph):
    min_dist = sys.maxsize
    best_start = 0
    for i in range(len(graph) - 1):
        dist = nearest_neighbor(graph, i)[1]
        if dist < min_dist:
            min_dist = dist
            best_start = i
    return nearest_neighbor(graph, best_start)

df1 = pd.read_csv('Data/Dane_TSP_48.csv')
df2 = pd.read_csv('Data/Dane_TSP_76.csv')
df3 = pd.read_csv('Data/Dane_TSP_127.csv')

print("Najlepsza kolejność miast:", best_path(df3)[0])
print("Najlepsza odległość:", best_path(df3)[1])
