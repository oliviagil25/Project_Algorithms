import sys
import pandas as pd
import numpy as np
import NN

#Wczytanie danych
df = pd.read_csv('C:/Users/olivv/OneDrive/Pulpit/Dane_TSP_48.csv')

#Utworzenie na razie pustego planu podróży
itinerary = {
    "city": [],
    "distance": []
}

if __name__ == '__main__':
    NN.NN_method(df, itinerary)
    print(NN.NN_method(df, itinerary))
    print(itinerary)


