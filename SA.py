import math
import random
import pandas as pd

# Obliczanie całkowitej długości trasy na podstawie ramki danych z odległościami między miastami
def total_distance(distances_df, order):
    total = 0
    for i in range(len(order) - 1):
        total += distances_df.iloc[order[i], order[i+1]]
    total += distances_df.iloc[order[-1], order[0]]  # Dodanie odległości z powrotem do punktu początkowego
    return total

# Algorytm symulowanego wyżarzania
def simulated_annealing(distances_df, initial_temp, final_temp, alpha, max_iter):
    num_cities = len(distances_df)
    current_order = list(range(num_cities))
    random.shuffle(current_order)  # Losowa permutacja miast
    current_distance = total_distance(distances_df, current_order)

    temperature = initial_temp
    iteration = 0

    while temperature > final_temp and iteration < max_iter:
        next_order = current_order.copy()

        # Zamiana losowych dwóch miast
        swap_indices = sorted(random.sample(range(num_cities), 2))
        next_order[swap_indices[0]], next_order[swap_indices[1]] = next_order[swap_indices[1]], next_order[swap_indices[0]]

        next_distance = total_distance(distances_df, next_order)

        delta = next_distance - current_distance
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_order = next_order
            current_distance = next_distance

        temperature *= alpha
        iteration += 1

    return current_order, current_distance

distances_df = pd.read_csv('C:/Users/olivv/OneDrive/Pulpit/Dane_TSP_48.csv')

# Uruchomienie algorytmu
temperatures = ([1000, 2000, 5000, 10000])
alphas = ([0.9, 0.95, 0.975, 0.99])
num_of_iterations = ([1000, 2000, 5000, 10000])

def temperature_influence(temperatures):
    for i in temperatures:
        best_order, best_distance = simulated_annealing(distances_df, i,  1, 0.975, 1000)
        print("Temperatura:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)

def alpha_influence(alphas):
    for i in alphas:
        best_order, best_distance = simulated_annealing(distances_df, 1000, 1, i, 1000)
        print("Alfa:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)

def num_of_iterations_influence(num_of_iterations):
    for i in num_of_iterations:
        best_order, best_distance = simulated_annealing(distances_df, 1000, 1, 0.975, i)
        print("Liczba iteracji:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)

