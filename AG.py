import random
import pandas as pd
import xlsxwriter

#wczytanie pliku excel
nazwaPliku = "/dane/Dane29.xlsx"
daneExcela = pd.read_excel(nazwaPliku)
wartosci = daneExcela.values
odleglosc = {f"{x + 1}:{y}": wartosci[x, y] for y in range(1, len(wartosci) + 1) for x in range(len(wartosci))}

odleglosci_miedzy_miastami = odleglosc
miasta = list(range(1, len(wartosci) + 1))

#parametry wraz z ich wartościami
rozmiarPopulacji = [50, 150, 250]
prawdopodobienstwoMutacji = [0.2, 0.3, 0.4]
liczbaIteracji = [500, 1000, 1500]
rozmiarTurnieju = 5
rozmiarElity = 2

#oblicza odleglosc miedzy miastami
def odleglosc(a, b):
    return odleglosci_miedzy_miastami.get(f'{a}:{b}', odleglosci_miedzy_miastami.get(f'{b}:{a}', 0))

#ta funkcja ocenia trase poprzez sume odleglosci miedzy kolejnymi miastami
def ocena(trasa):
    suma = 0
    for i in range(len(trasa)):
        suma += odleglosc(trasa[i], trasa[(i + 1) % len(trasa)])
    return suma

#funkcja ktora generuje poczatkowa populacje
def generuj_poczatkowa_populacje(rozmiarPopulacji):
    populacja = []
    for _ in range(rozmiarPopulacji):
        trasa = miasta.copy()
        random.shuffle(trasa)
        populacja.append(trasa)
    return populacja

#przeprowadza turniej, z którego wyłaniany jest najlepszy osobnik.
def turniej(populacja, rozmiar_turnieju):
    turniej = random.sample(populacja, min(rozmiar_turnieju, len(populacja)))
    zwyciezca = min(turniej, key=lambda trasa: ocena(trasa))
    return zwyciezca

#funckja ktora pozwala wybrac najlepszego potomka
def krzyzowanie(rodzic1, rodzic2):
    punkt1 = random.randint(0, len(rodzic1) - 1)
    punkt2 = random.randint(punkt1, len(rodzic1) - 1)
    potomek = [-1] * len(rodzic1)

    potomek[punkt1:punkt2 + 1] = rodzic1[punkt1:punkt2 + 1]
    indeks = punkt2 + 1

    for miasto in rodzic2 + rodzic2:
        if miasto not in potomek:
            potomek[indeks % len(potomek)] = miasto
            indeks += 1

    return potomek

#przeprowadzana mutacja z danym prawdopodobienstwem
def mutacja(trasa, prawdopodobienstwo_mutacji):
    if random.random() < prawdopodobienstwo_mutacji:
        punkt1 = random.randint(0, len(trasa) - 1)
        punkt2 = random.randint(punkt1, len(trasa) - 1)
        trasa[punkt1:punkt2 + 1] = reversed(trasa[punkt1:punkt2 + 1])

def algorytm_genetyczny(prawdopodobienstwo_mutacji, liczbaIteracji, rozmiarPopulacji):
    populacja = generuj_poczatkowa_populacje(rozmiarPopulacji)

    for _ in range(liczbaIteracji):
        populacja.sort(key=lambda trasa: ocena(trasa))

        nowa_populacja = populacja[:rozmiarElity]

        while len(nowa_populacja) < rozmiarPopulacji:
            rodzic1 = turniej(populacja, rozmiarTurnieju)
            rodzic2 = turniej(populacja, rozmiarTurnieju)

            potomek1 = krzyzowanie(rodzic1, rodzic2)
            potomek2 = krzyzowanie(rodzic2, rodzic1)

            mutacja(potomek1, prawdopodobienstwo_mutacji)
            mutacja(potomek2, prawdopodobienstwo_mutacji)

            nowa_populacja.extend([potomek1, potomek2])

        populacja = nowa_populacja

    najlepsza_trasa = min(populacja, key=lambda trasa: ocena(trasa))
    return najlepsza_trasa

wyniki = []

for pm in prawdopodobienstwoMutacji:
    for li in liczbaIteracji:
        for rp in rozmiarPopulacji:
            najlepsza_trasa = algorytm_genetyczny(pm, li, rp)
            ocena_trasy = ocena(najlepsza_trasa)
            wyniki.append({
                'prawdopodobienstwoMutacji': pm,
                'liczbaIteracji': li,
                'rozmiarPopulacji': rp,
                'trasa': najlepsza_trasa,
                'ocenaTrasy': ocena_trasy
            })

#wyniki posortowane od najmniejszej wartosci do najwiekszej
wyniki_posortowane = sorted(wyniki, key=lambda x: x['ocenaTrasy'])

#zapis wynikow do nowo stworzonego pliku excel
arkuszRoboczy = xlsxwriter.Workbook(nazwaPliku.replace('.xlsx', '_wyniki.xlsx'))
arkuszDanych = arkuszRoboczy.add_worksheet()
arkuszDanych.set_column(6, 6)

wiersz = 1
for wynik in wyniki_posortowane:
    arkuszDanych.write(wiersz, 0, wynik['prawdopodobienstwoMutacji'])
    arkuszDanych.write(wiersz, 1, wynik['liczbaIteracji'])
    arkuszDanych.write(wiersz, 2, wynik['rozmiarPopulacji'])
    arkuszDanych.write(wiersz, 3, wynik['ocenaTrasy'])
    arkuszDanych.write(wiersz, 4, ','.join(str(point) for point in wynik['trasa']))
    wiersz += 1

arkuszRoboczy.close()
