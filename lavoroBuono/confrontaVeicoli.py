from Levenshtein import distance as levenshtein_distance
import math
import json
from tokenizzazioneStemming import tokenStem as tS  # Assumiamo che tokenStem sia la funzione importata da tokenStem.py
from tokenizzazioneStemming import \
    levenstein as lev  # Assumiamo che tokenStem sia la funzione importata da tokenStem.py


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


# Funzione per calcolare la similitudine tra due JSON basati sulla struttura fornita
def calcola_similitudine(json1, json2):
    distanze = []

    # Calcolo della distanza geografica
    distanza_geo = calcola_distanza_geografica(json1['location']['latitude'], json1['location']['longitude'],
                                               json2['location']['latitude'], json2['location']['longitude'])
    distanze.append(distanza_geo)

    # Calcolo della distanza tra i nomi delle strade
    # Utilizza la funzione tokenStem e la distanza di Levenshtein
    for strada1, strada2 in zip(json1['toponomy']['streetNames'], json2['toponomy']['streetNames']):
        stemmed_strada1 = tS([strada1])[0]
        stemmed_strada2 = tS([strada2])[0]
        distanza_strade = levenshtein_distance(stemmed_strada1, stemmed_strada2)
        distanze.append(distanza_strade)

    # Calcolo dell'indice di similitudine come media delle distanze
    indice = sum(distanze) / len(distanze)
    return indice


def leggi_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


json1 = leggi_json("../auto1.json")
json2 = leggi_json("../auto2.json")

# Calcola e stampa l'indice di similitudine
indice_similitudine = calcola_similitudine(json1, json2)
print(f"L'indice di similitudine tra i due veicoli è: {indice_similitudine}")

# Determinazione se i veicoli si stanno avvicinando allo stesso incrocio
soglia = 0.5  # La soglia deve essere definita empiricamente
if indice_similitudine < soglia:
    print("I due veicoli sono probabilmente diretti verso lo stesso incrocio.")
else:
    print("I due veicoli non sembrano diretti verso lo stesso incrocio.")

# Definizione di una soglia di similitudine
# La soglia può essere definita empiricamente. Per esempio, dopo aver testato con diversi JSON,
# si può stabilire che una soglia di similitudine di X indica efficacemente che due veicoli
# si stanno avvicinando allo stesso incrocio.
