import pandas as pd
import random
import xlsxwriter
from itertools import product

def dlugosc_trasy(trasa, odleglosc):
    dlugosc = sum([odleglosc[f"{punkt_startowy}:{punkt_docelowy}"]
                   for punkt_startowy, punkt_docelowy in zip(trasa[:-1], trasa[1:])])
    return dlugosc

def wykonaj_ruch(trasa, p1, p2, rodzaj_ruchu):
    i1 = trasa.index(p1)
    i2 = trasa.index(p2)

    if (i1 > i2):
        i1, i2 = i2, i1

    if rodzaj_ruchu == 'zamiana':
        trasa[i1], trasa[i2] = trasa[i2], trasa[i1]
    elif rodzaj_ruchu == 'odwrocenie':
        reverseLength = int(round(i2 - i1) / 2)
        for i in range(reverseLength):
            trasa[i1 + i], trasa[i2 - i] = trasa[i2 - i], trasa[i1 + i]


def nowa_dlugosc_trasy(trasa, odleglosc, aktualnadlugosc, p1, p2):
    i1 = trasa.index(p1)
    i2 = trasa.index(p2)

    if (i1 > i2):
        i1, i2 = i2, i1

    if (i1 == 0):
        aktualnadlugosc -= odleglosc[f"{trasa[-1]}:{trasa[i1]}"]
    else:
        aktualnadlugosc -= odleglosc[f"{trasa[i1 - 1]}:{trasa[i1]}"]
    aktualnadlugosc -= odleglosc[f"{trasa[i1]}:{trasa[i1 + 1]}"]

    if (i2 == len(trasa) - 1):
        aktualnadlugosc -= odleglosc[f"{trasa[i2]}:{trasa[0]}"]
    else:
        aktualnadlugosc -= odleglosc[f"{trasa[i2]}:{trasa[i2 + 1]}"]
    aktualnadlugosc -= odleglosc[f"{trasa[i2 - 1]}:{trasa[i2]}"]

    trasa[i1], trasa[i2] = trasa[i2], trasa[i1]

    if (i1 == 0):
        aktualnadlugosc += odleglosc[f"{trasa[-1]}:{trasa[i1]}"]
    else:
        aktualnadlugosc += odleglosc[f"{trasa[i1 - 1]}:{trasa[i1]}"]
    aktualnadlugosc += odleglosc[f"{trasa[i1]}:{trasa[i1 + 1]}"]

    if (i2 == len(trasa) - 1):
        aktualnadlugosc += odleglosc[f"{trasa[i2]}:{trasa[0]}"]
    else:
        aktualnadlugosc += odleglosc[f"{trasa[i2]}:{trasa[i2 + 1]}"]
    aktualnadlugosc += odleglosc[f"{trasa[i2 - 1]}:{trasa[i2]}"]

    trasa[i1], trasa[i2] = trasa[i2], trasa[i1]

    return {"p1": p1, "p2": p2, "dlugosc": aktualnadlugosc}


def dlugosc_odwroceniu(trasa, odleglosc, aktualnadlugosc, p1, p2):
    i1 = trasa.index(p1)
    i2 = trasa.index(p2)

    if (i1 > i2):
        i1, i2 = i2, i1

    wykonaj_ruch(trasa, p1, p2, 'odwrocenie')
    aktualnadlugosc = dlugosc_trasy(trasa, odleglosc)
    wykonaj_ruch(trasa, p1, p2,'odwrocenie')

    return {"p1": p1, "p2": p2, "dlugosc": aktualnadlugosc}


def czy_ruch_tabu(listaTabu, mozliwyRuch):
    if not listaTabu:
        return False

    p1, p2 = mozliwyRuch['p1'], mozliwyRuch['p2']

    for ruchTabu in listaTabu:
        if {p1, p2} == set(ruchTabu):
            return True
    return False

listaIteracji = [100,250,500,750]
listaBrakuPoprawy = [4,8,16,""]
dlugoscListyTabu = [3,4,5]
rodzajSasiedztwa = ["zamiana", "odwrocenie"]

kombinacjeParametrow = [{'iteracje': iteracje, 'brakPoprawy': brakPoprawy, 'dlugoscTabu': dlugoscTabu, 'sasiedztwo': sasiedztwo}
                        for iteracje, brakPoprawy, dlugoscTabu, sasiedztwo
                        in product(listaIteracji, listaBrakuPoprawy, dlugoscListyTabu, rodzajSasiedztwa)]

nazwaPliku = "/dane/Dane_TSP_48.xlsx"
daneExcela = pd.read_excel(nazwaPliku)
wartosci = daneExcela.values
odleglosc = {}
odleglosc = {f"{x + 1}:{y}": wartosci[x, y] for y in range(1, len(wartosci) + 1) for x in range(len(wartosci))}

wyniki = []
przerwanieBezPoprawy = False

for parametry in kombinacjeParametrow:

    przerwanieBezPoprawy = "brak"

    obecnyBrakPoprawy = 0
    trasa = list(range(1, len(wartosci) + 1))

    random.shuffle(trasa)
    dlugoscStartowa = dlugosc_trasy(trasa, odleglosc)
    aktualnadlugosc = dlugoscStartowa
    listaTabu = []
    najlepszaTrasa = {'trasa': trasa.copy(), 'dlugosc': aktualnadlugosc}

    for i in range(parametry['iteracje']):
        if obecnyBrakPoprawy == parametry['brakPoprawy']:
            przerwanieBezPoprawy = i
            break

        najlepszeRuchy = [{"p1": 0, "p2": 0, "dlugosc": float('inf')}] * (parametry['dlugoscTabu'] + 1)

        for p1 in range(1, len(trasa) + 1):
            for p2 in range(p1 + 1, len(trasa) + 1):
                rodzaj_sasiedztwa = parametry['sasiedztwo']

                if rodzaj_sasiedztwa == 'zamiana':
                    mozliwyRuch = nowa_dlugosc_trasy(trasa, odleglosc, aktualnadlugosc, p1, p2)
                elif rodzaj_sasiedztwa == 'odwrocenie':
                    mozliwyRuch = dlugosc_odwroceniu(trasa, odleglosc, aktualnadlugosc, p1, p2)
                    mozliwyRuch['dlugosc'] = nowa_dlugosc_trasy(trasa, odleglosc, mozliwyRuch['dlugosc'], p1, p2)[
                        'dlugosc']

                if mozliwyRuch['dlugosc'] < najlepszeRuchy[-1]['dlugosc']:
                    najlepszeRuchy[-1] = mozliwyRuch
                    najlepszeRuchy.sort(key=lambda r: r['dlugosc'])

        for mozliwyRuch in najlepszeRuchy:
            if not czy_ruch_tabu(listaTabu, mozliwyRuch):
                if mozliwyRuch['dlugosc'] > aktualnadlugosc:
                    obecnyBrakPoprawy += 1
                else:
                    obecnyBrakPoprawy = 0
                listaTabu.insert(0, [mozliwyRuch['p1'], mozliwyRuch['p2']])
                if len(listaTabu) == parametry['dlugoscTabu'] + 1:
                    del listaTabu[-1]

                wykonaj_ruch(trasa, mozliwyRuch['p1'], mozliwyRuch['p2'], parametry['sasiedztwo'])

                aktualnadlugosc = mozliwyRuch['dlugosc']
                if najlepszaTrasa['dlugosc'] > aktualnadlugosc:
                    najlepszaTrasa['dlugosc'] = aktualnadlugosc
                    najlepszaTrasa['trasa'] = trasa.copy()
                break

    parametry['przerwanieBezPoprawy'] = przerwanieBezPoprawy
    wyniki.append({'parametry': parametry, 'najlepszaDlugoscTrasy': najlepszaTrasa['dlugosc'], 'trasa': najlepszaTrasa['trasa']})

wyniki = sorted(wyniki, key=lambda d: d['najlepszaDlugoscTrasy'])

dlugosc_trasy = len(','.join(str(point) for point in wyniki[0]['trasa']))
dlugosc_trasy = int(0.85 * dlugosc_trasy)
arkuszRoboczy = xlsxwriter.Workbook(nazwaPliku)
arkuszDanych = arkuszRoboczy.add_worksheet()
arkuszDanych.set_column(6, 6, dlugosc_trasy)

wiersz = 1
for wynik in wyniki:
    arkuszDanych.write(wiersz, 0, wynik['parametry']['iteracje'])
    arkuszDanych.write(wiersz, 1, wynik['parametry']['brakPoprawy'])
    arkuszDanych.write(wiersz, 2, wynik['parametry']['dlugoscTabu'])
    arkuszDanych.write(wiersz, 3, wynik['parametry']['sasiedztwo'])
    arkuszDanych.write(wiersz, 4, wynik['najlepszaDlugoscTrasy'])
    arkuszDanych.write(wiersz, 5, ','.join(str(point) for point in wynik['trasa']))
    wiersz += 1

arkuszRoboczy.close()
