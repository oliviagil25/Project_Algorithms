import pandas as pd
import numpy as np
import random
import xlsxwriter

#wczytanie pliku excel
if __name__ == "__main__":
    nazwaPliku = "C:/Users/Ania/Documents/studia/semestr5/IO/Dane_TSP_127.xlsx"
    daneExcela = pd.read_excel(nazwaPliku)
    wartosci = daneExcela.values
    odleglosc = {f"{x + 1}:{y}": wartosci[x, y] for y in range(1, len(wartosci) + 1) for x in range(len(wartosci))}

    #parametry
    liczby_iteracji = [100, 250, 500, 750]
    rodzaje_sasiedztwa = ["swap_cities", "insert_city", "reverse_order"]
    startowe_miasta = list(range(1, len(wartosci) + 1))


#funkcja licząca odelgłość pomiędzy miastami
def odleglosc_miasta(miasto_a, miasto_b, odleglosc):
    return odleglosc[f"{miasto_a}:{miasto_b}"]

#funkcja sumująca odległośći
def oblicz_trase(trasa, odleglosc):
    return sum(odleglosc_miasta(trasa[i], trasa[i + 1], odleglosc) for i in range(len(trasa) - 1))

#funkcja wykonująca ruch w zależności od rodzaju sąsiedztwa
def jakie_sasiedztwo(trasa, rodzaj_sasiedztwa):
    sasiedztwo = []

    if rodzaj_sasiedztwa == "swap_cities":
        sasiedztwo = [trasa[:i] + [trasa[j]] + trasa[i+1:j] + [trasa[i]] + trasa[j+1:] for i in range(len(trasa)) for j in range(i + 1, len(trasa))]

    elif rodzaj_sasiedztwa == "insert_city":
        sasiedztwo = [trasa[:j] + [trasa[i]] + trasa[j:] for i in range(len(trasa)) for j in range(len(trasa) + 1) if j != i]

    elif rodzaj_sasiedztwa == "reverse_order":
        sasiedztwo = [trasa[:i] + trasa[i:j + 1][::-1] + trasa[j + 1:] for i in range(len(trasa)) for j in range(i + 1, len(trasa))]

    return sasiedztwo

def algorytm_wspinaczka(odleglosc, liczby_iteracji, rodzaje_sasiedztwa, startowe_miasta):
    wyniki = []

    for liczba_iter in liczby_iteracji:
        for rodzaj_sas in rodzaje_sasiedztwa:
            aktualne_miasta = startowe_miasta.copy()
            odleglosc_aktualna = oblicz_trase(aktualne_miasta, odleglosc)

            for _ in range(liczba_iter):
                sasiedztwo = jakie_sasiedztwo(aktualne_miasta, rodzaj_sas)
                random.shuffle(sasiedztwo)

                for sasiad in sasiedztwo:
                    odleglosc_sasiada = oblicz_trase(sasiad, odleglosc)

                    if odleglosc_sasiada < odleglosc_aktualna:
                        aktualne_miasta = sasiad
                        odleglosc_aktualna = odleglosc_sasiada

                        # sprawdzenie czy trasa jest już w wynikach
                        if any(np.array_equal(wynik["Trasa"], sasiad) for wynik in wyniki):
                            continue

                        # przedstawienie wyników
                        wyniki.append({
                            "Parametry": {
                                "liczba_iter": liczba_iter,
                                "rodzaj_sas": rodzaj_sas
                            },
                            "Trasa": sasiad,
                            "Odległość": odleglosc_sasiada
                        })

    # wyświetlenie wyników w kolejności rosnącej- najlepsze, najkrótsze odległości są pierwsze w kolejności
    wyniki.sort(key=lambda x: x["Odległość"])

    return wyniki

    wyniki = algorytm_wspinaczka(odleglosc, liczby_iteracji, rodzaje_sasiedztwa, startowe_miasta)

    # zapis wyników do nowego pliku Excel
    nazwaPlikuWyniki = nazwaPliku.replace('.xlsx', '_wyniki.xlsx')
    arkuszRoboczy = xlsxwriter.Workbook(nazwaPlikuWyniki)
    arkuszDanych = arkuszRoboczy.add_worksheet()
    arkuszDanych.set_column(0, 2, 20)  # ustawienie szerokości kolumny

    # nagłówki
    naglowki = ['Liczba Iteracji', 'Rodzaj Sasiedztwa', 'Odległość', 'Trasa']
    for k, naglowek in enumerate(naglowki):
        arkuszDanych.write(0, k, naglowek)

    wiersz = 1
    for wynik in wyniki:
        arkuszDanych.write(wiersz, 0, wynik["Parametry"]["liczba_iter"])
        arkuszDanych.write(wiersz, 1, wynik["Parametry"]["rodzaj_sas"])
        arkuszDanych.write(wiersz, 2, wynik["Odległość"])
        arkuszDanych.write(wiersz, 3, ','.join(str(point) for point in wynik["Trasa"]))
        wiersz += 1

    arkuszRoboczy.close()

