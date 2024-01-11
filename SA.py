import math
import random
import pandas as pd
import NN

#wczytywanie plików
df1 = pd.read_csv('Data/Dane_TSP_48.csv')
df2 = pd.read_csv('Data/Dane_TSP_76.csv')
df3 = pd.read_csv('Data/Dane_TSP_127.csv')

#parametry
temperatures = ([50, 100, 500, 2000])
alphas = ([0.75, 0.85, 0.95, 0.99])
num_of_iterations = ([100, 1000, 5000, 10000])

#funkcja licząca całkowitą długość trasy
def total_distance(distances_df, order):
    total = 0
    for i in range(len(order) - 1):
        total += distances_df.iloc[order[i], order[i+1]]
    total += distances_df.iloc[order[-1], order[0]]  #dodanie odległości z powrotem do punktu początkowego
    return total

#funkcja używana, jeśli chcemy zastosować algorytm dla losowej kolejności miast
def random_order(df):
    num_cities = len(df)
    order = list(range(num_cities))
    return order

def simulated_annealing(order, distances_df, initial_temp, final_temp, alpha, max_iter):
    num_cities = len(distances_df)
    current_order = order
    current_distance = total_distance(distances_df, current_order)

    temperature = initial_temp
    iteration = 0

    while temperature > final_temp and iteration < max_iter:
        next_order = current_order.copy()

        # swap cities
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

def temperature_influence(temperatures):
    for i in temperatures:
        best_order, best_distance = simulated_annealing(NN.best_path(df1)[0], df1, i,  1, 0.975, 1000)
        print("Temperatura:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)

def alpha_influence(alphas):
    for i in alphas:
        best_order, best_distance = simulated_annealing(NN.best_path(df1)[0], df1, 1000, 1, i, 1000)
        print("Alfa:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)

def num_of_iterations_influence(num_of_iterations):
    for i in num_of_iterations:
        best_order, best_distance = simulated_annealing(NN.best_path(df1)[0], df1, 1000, 1, 0.975, i)
        print("Liczba iteracji:", i)
        print("Najlepsza kolejność miast:", best_order)
        print("Najlepsza odległość:", best_distance)


best_order, best_distance = simulated_annealing(NN.best_path(df3)[0], df3, 100, 1, 0.975, 1000)
print("Najlepsza kolejność miast:", best_order)
print("Najlepsza odległość:", best_distance)