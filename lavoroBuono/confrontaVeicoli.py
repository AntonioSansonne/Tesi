from Levenshtein import distance as levenshtein_distance
import math
import json
from tokenStem import tokenStem as tS
from tokenStem import levenstein as lev


# Calcola la distanza geografica tra due punti utilizzando le loro coordinate latitudinali e longitudinali
def calcola_distanza_geografica(lat1, lon1, lat2, lon2):
    """
    Utilizza la formula di Haversine per calcolare la distanza tra due punti sulla terra. La formula considera la
    sfericità della Terra per calcolare la distanza più breve tra i punti lungo la superficie del globo.
    """
    # Raggio della Terra in km
    R = 6371.0

    # Conversione delle coordinate da gradi a radianti
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differenza delle coordinate
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Calcolo utilizzando la formula di Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distanza totale in km
    distance = R * c
    return distance

def confronta_strade(json1, json2):
    strade_auto1 = json1['toponomy']['streetNames']
    strade_auto2 = json2['toponomy']['streetNames']

    # Controlla se le due liste di strade sono uguali
    if strade_auto1 == strade_auto2:
        return True

    # Controlla se le due liste di strade sono inverse l'una dell'altra
    if strade_auto1 == strade_auto2[::-1]:
        return True

    # Se nessuna delle condizioni precedenti è verificata, le auto non si stanno dirigendo verso lo stesso incrocio
    return False


def confronta_dettagliato_strade(strade_auto1, strade_auto2):
    # Controlla se le lunghezze delle due liste sono diverse
    if len(strade_auto1) != len(strade_auto2):
        return False

    # Confronta le liste delle strade elemento per elemento
    for i in range(len(strade_auto1)):
        # Se le strade non corrispondono in posizione e ordine, le auto non si stanno dirigendo verso lo stesso incrocio
        if strade_auto1[i] != strade_auto2[i]:
            return False

    # Se il confronto è andato bene, le auto si stanno dirigendo verso lo stesso incrocio
    return True


def si_incontrano_all_incrocio(json1, json2):
    # Ottieni le strade dei due veicoli
    strade_auto1 = json1['toponomy']['streetNames']
    strade_auto2 = json2['toponomy']['streetNames']

    # Controlla se le strade si intersecano
    if strade_auto1[-1] == strade_auto2[-1] and strade_auto1[-2] == strade_auto2[-2]:
        return True  # Le strade si intersecano

    return False  # Le strade non si intersecano


# Funzione per calcolare la similitudine tra due JSON basati sulla struttura fornita
def calcola_similitudine(json1, json2):
    distanze = []

    # Calcolo della distanza geografica
    distanza_geo = calcola_distanza_geografica(json1['location']['latitude'], json1['location']['longitude'],
                                               json2['location']['latitude'], json2['location']['longitude'])
    distanze.append(distanza_geo)

    # if si_incontrano_all_incrocio(json1, json2):
    #     # Se si, restituisci una similitudine massima
    #     return 1.0
    # else:
    #     # Altrimenti, calcola una similitudine basata sulla distanza geografica
    #     return 1.0 / (1.0 + distanza_geo)  # Esempio di calcolo di similitudine basato sulla distanza

    # # Utilizzo della funzione confronta_strade per determinare se le auto si stanno dirigendo verso lo stesso incrocio
    # if confronta_strade(json1, json2):
    #     print("ALe due auto si stanno dirigendo verso lo stesso incrocio.")
    # else:
    #     print("ALe due auto non si stanno dirigendo verso lo stesso incrocio.")

    # Calcolo della distanza tra i nomi delle strade
    # Utilizza la funzione tokenStem e la distanza di Levenshtein
    for strada1, strada2 in zip(json1['toponomy']['streetNames'], json2['toponomy']['streetNames']):
        stemmed_strada1 = tS([strada1])[0]
        print("strada1: "+stemmed_strada1)
        stemmed_strada2 = tS([strada2])[0]
        print("strada2: "+stemmed_strada2)
        distanza_strade = levenshtein_distance(stemmed_strada1, stemmed_strada2)
        print("distanze strade: ", distanza_strade)
        distanze.append(distanza_strade)

    # stemmed = []
    # for strada1, strada2 in zip(json1['toponomy']['streetNames'], json2['toponomy']['streetNames']):
    #     stemmed.append(tS([strada1])[0])
    #     print("\nstemmed 1: ",stemmed)
    #     stemmed.append(tS([strada2])[0])
    #     print("\nstemmed 2: ",stemmed)
    #     distanza_strade = lev(stemmed)
    #     print("\ndistanze strade: ", distanza_strade)
    #     distanze.append(distanza_strade)
    # print("\ndistanze: ",distanze)
    # print("sum distanze:", sum(distanze))
    # print("len distanze:", len(distanze))


    # # Verifica se le strade si intersecano
    # strade_auto1 = json1['toponomy']['streetNames']
    # strade_auto2 = json2['toponomy']['streetNames']
    # intersezione_strade = False
    # for strada1 in strade_auto1:
    #     for strada2 in strade_auto2:
    #         # Confronto diretto tra le strade
    #         if strada1 == strada2:
    #             intersezione_strade = True
    #             break
    #     if intersezione_strade:
    #         break

    # Calcolo dell'indice di similitudine come media delle distanze
    indice = sum(distanze) / len(distanze)
    # indice = 1.0 / (1.0 + distanza_geo) if intersezione_strade else 0.0
    return indice


def leggi_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


json1 = leggi_json("../jsonFile/auto11.json")
json2 = leggi_json("../jsonFile/auto12.json")

# Calcola e stampa l'indice di similitudine
indice_similitudine = calcola_similitudine(json1, json2)
print(f"L'indice di similitudine tra i due veicoli è: {indice_similitudine}")

# Determinazione se i veicoli si stanno avvicinando allo stesso incrocio
soglia = 1  # La soglia deve essere definita empiricamente
if indice_similitudine <= soglia:
    print("I due veicoli sono probabilmente diretti verso lo stesso incrocio.")
else:
    print("I due veicoli non sembrano diretti verso lo stesso incrocio.")

# Definizione di una soglia di similitudine
# La soglia può essere definita empiricamente. Per esempio, dopo aver testato con diversi JSON,
# si può stabilire che una soglia di similitudine di X indica efficacemente che due veicoli
# si stanno avvicinando allo stesso incrocio.
