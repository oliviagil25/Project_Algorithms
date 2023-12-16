#C:\Users\olivv\OneDrive\Pulpit\Studia
import sys
import pandas as pd
import numpy as np

#Wczytanie danych
df = pd.read_csv('C:/Users/olivv/OneDrive/Pulpit/Dane_TSP_48.csv')

#Dodanie kolumny oznaczającej czy miasto było już odwiedzone
#df['unvisited'] = True

minimal_distance = sys.maxsize
itinerary = {
    "city": [],
    "distance": []
}

#metoda pozwala określić, do którego miasta jest najbliżej w danym momencie
def next_city(row, unvisited):
    df = pd.DataFrame({'Row': row, 'Unvisited': unvisited})
    df = df.sort_values(by='Row')
    for i in range(0,len(df)):
        if ((df[i]['Row'] != 0) and (unvisited[i]['Unvisited'] is True)):
            break
    value = df[i]['Row']
    column = row[row == value].index[0]
    return value, column

def NN_method(dataframe):
    #rozważamy możliwość rozpoczęcia trasy w każdym mieście
    for i in dataframe.rows:
        unvisited = [True] * len(dataframe)
        sum = 0
        cities = []
        distances = []
        for j in range(0, len(dataframe)):
            distances[j] = next_city(df.loc[j], unvisited)[0]
            cities[j] = next_city(df.loc[j], unvisited)[1]
            sum=sum+distances[j]
        sum=sum+dataframe.loc[i,cities[j]] #odległość od ostatniego do pierwszego miasta
        if sum<minimal_distance:
            minimal_distance = sum
            itinerary["city"].append(cities)
            itinerary["distance"].append(distances)


if __name__ == '__main__':
    print(1)


