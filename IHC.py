import pandas as pd
import numpy as np
import random
import xlsxwriter

def odleglosc_miasta(miasto_a, miasto_b, odleglosc):
    return odleglosc[f"{miasto_a}:{miasto_b}"]

def oblicz_trase_odleglosc(trasa, odleglosc):
    return sum(odleglosc_miasta(trasa[i], trasa[i + 1], odleglosc) for i in range(len(trasa) - 1))

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
            odleglosc_aktualna = oblicz_trase_odleglosc(aktualne_miasta, odleglosc)

            for _ in range(liczba_iter):
                sasiedztwo = jakie_sasiedztwo(aktualne_miasta, rodzaj_sas)
                random.shuffle(sasiedztwo)

                for sasiad in sasiedztwo:
                    odleglosc_sasiada = oblicz_trase_odleglosc(sasiad, odleglosc)

                    if odleglosc_sasiada < odleglosc_aktualna:
                        aktualne_miasta = sasiad
                        odleglosc_aktualna = odleglosc_sasiada

                        # Sprawdzam czy trasa (miasto??) jest już w wynikach nie
                        if any(np.array_equal(wynik["Trasa"], sasiad) for wynik in wyniki):
                            continue

                        # Wyniki
                        wyniki.append({
                            "Parametry": {
                                "liczba_iter": liczba_iter,
                                "rodzaj_sas": rodzaj_sas
                            },
                            "Trasa": sasiad,
                            "Odległość": odleglosc_sasiada
                        })

    # Ustawienie wyników w kolejności malejącej - widoczne najlepsze wyniki
    wyniki.sort(key=lambda x: x["Odległość"])

    return wyniki

if __name__ == "__main__":
    nazwaPliku = "C:/Users/Ania/Documents/studia/semestr5/IO/Dane_TSP_127.xlsx"
    daneExcela = pd.read_excel(nazwaPliku)
    wartosci = daneExcela.values
    odleglosc = {f"{x + 1}:{y}": wartosci[x, y] for y in range(1, len(wartosci) + 1) for x in range(len(wartosci))}

    liczby_iteracji = [100, 250, 500, 750]
    rodzaje_sasiedztwa = ["swap_cities", "insert_city", "reverse_order"]
    startowe_miasta = list(range(1, len(wartosci) + 1))

    wyniki = algorytm_wspinaczka(odleglosc, liczby_iteracji, rodzaje_sasiedztwa, startowe_miasta)

    # Zapisanie wyników do pliku Excel
    nazwaPlikuWyniki = nazwaPliku.replace('.xlsx', '_wyniki.xlsx')
    arkuszRoboczy = xlsxwriter.Workbook(nazwaPlikuWyniki)
    arkuszDanych = arkuszRoboczy.add_worksheet()
    arkuszDanych.set_column(0, 2, 20)  # Ustawienie szerokości kolumny

    # Nagłówki
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

