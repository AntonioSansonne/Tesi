from nltk.stem import PorterStemmer
import re
from Levenshtein import distance as levenshtein_distance
import json
# Prima di procedere con le modifiche al codice, carichiamo e visualizziamo i contenuti dei nuovi file JSON forniti dall'utente.
# Questo ci aiuterà a comprendere la struttura dei dati e come applicare le modifiche richieste.

# Percorsi dei file JSON forniti
auto11_json_path = '../jsonFile/auto10.json'
auto12_json_path = '../jsonFile/auto13.json'

# Caricamento e visualizzazione dei contenuti dei file JSON


# Caricamento auto11.json
with open(auto11_json_path, 'r') as file:
    auto11_json = json.load(file)

# Caricamento auto12.json
with open(auto12_json_path, 'r') as file:
    auto12_json = json.load(file)

auto11_json, auto12_json


# Funzione per la tokenizzazione e lo stemming dei nomi delle strade
def tokenStem_street_names(street_names):
    stemmer = PorterStemmer()
    stemmed_names = []
    for name in street_names:
        tokens = re.findall(r'\w+', name.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        stemmed_name = " ".join(stemmed_tokens)
        stemmed_names.append(stemmed_name)
    return stemmed_names

# Applicazione della tokenizzazione e dello stemming ai nomi delle strade dei due veicoli
auto11_streets_stemmed = tokenStem_street_names(auto11_json['toponomy']['streetNames'])
auto12_streets_stemmed = tokenStem_street_names(auto12_json['toponomy']['streetNames'])

# Procediamo nuovamente con il confronto utilizzando la distanza di Levenshtein
levenshtein_distances = []
for street1 in auto11_streets_stemmed:
    for street2 in auto12_streets_stemmed:
        distance = levenshtein_distance(street1, street2)
        levenshtein_distances.append((street1, street2, distance))

# Filtriamo le coppie con distanza minore o uguale a una soglia (es. 2) per considerare una corrispondenza
threshold = 2
matches = [pair for pair in levenshtein_distances if pair[2] <= threshold]

# print("matches:", matches)


# Per creare un indice numerico che identifichi univocamente l'incrocio e determinare se i due veicoli si stanno dirigendo verso lo stesso incrocio,
# possiamo utilizzare una combinazione delle stringhe stemmate delle strade. In questo caso, dato che le corrispondenze sono esatte, possiamo
# assumere che l'incrocio sia univocamente identificato dai nomi delle strade coinvolti.

# Funzione per generare l'indice numerico dell'incrocio e determinare se i veicoli si stanno dirigendo verso lo stesso incrocio
def generate_intersection_index_and_direction(matches):
    # Generazione dell'indice univoco per l'incrocio, utilizzando i nomi delle strade stemmati
    intersection_index = "-".join(sorted([match[0] for match in matches]))

    # Determinazione se i veicoli si stanno dirigendo verso lo stesso incrocio
    # In questo contesto, dato che abbiamo già confrontato e trovato corrispondenze esatte, possiamo dire che si stanno dirigendo verso lo stesso incrocio
    if len(matches) > 0:
        direction_message = "I due veicoli sono probabilmente diretti verso lo stesso incrocio."
    else:
        direction_message = "I due veicoli non sembrano diretti verso lo stesso incrocio."
    # print("Indice: ", intersection_index)
    return intersection_index, direction_message


# Applicazione della funzione ai risultati del confronto
intersection_index, direction_message = generate_intersection_index_and_direction(matches)
# print(intersection_index)
print(direction_message)
