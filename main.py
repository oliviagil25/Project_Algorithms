import sys
import pandas as pd
import numpy as np

#Wczytanie danych
df = pd.read_csv('C:/Users/olivv/OneDrive/Pulpit/Dane_TSP_48.csv')

#Utworzenie na razie pustego planu podróży
itinerary = {
    "city": [],
    "distance": []
}

#metoda pozwala określić, do którego miasta należy w następnej kolejności pojechać oraz odległośc od niego
def next_city(row, unvisited):
    dfr = pd.DataFrame({'Row': row, 'Unvisited': unvisited})
    dfr = dfr.sort_values(by='Row', ascending=True)
    for i in range(0,len(dfr)):
        if ((dfr.iloc[i]['Row'] != 0) and (dfr.iloc[i]['Unvisited'] == True)):
            break
    value = dfr.iloc[i]['Row']
    for i, v in enumerate(row):
        if v == value:
            column = i
            break
    return value, column

#metoda najbliższego sąsiada: zwraca całkowitą długość trasy oraz uzupełnia plan podróży o kolejne miasta i odległości między nimi
def NN_method(dataframe):
    #rozważamy możliwość rozpoczęcia trasy w każdym mieście
    minimal_distance = sys.maxsize
    for i in range(0, len(dataframe)):
        unvisited = [True] * len(dataframe)
        sum_of_distances = 0
        cities = [0] * len(dataframe)
        distances = [0] * len(dataframe)
        a = i
        #pętla pozwalająca "poruszać się" od miasta do miasta
        for j in range(0, len(dataframe)):
            distances[j] = next_city(df.loc[a], unvisited)[0]
            cities[j] = next_city(df.loc[a], unvisited)[1]
            sum_of_distances=sum_of_distances+distances[j]
            unvisited[a] = False
            a = cities[j]
        sum_of_distances=sum_of_distances+dataframe.iloc[i,a] #odległość od ostatniego do pierwszego miasta
        if sum_of_distances<minimal_distance:
            minimal_distance = sum_of_distances
            cities.insert(0,i)
            itinerary["city"] = cities
            itinerary["distance"] = distances
    return sum_of_distances


if __name__ == '__main__':
    NN_method(df)
    print(NN_method(df))
    print(itinerary)


