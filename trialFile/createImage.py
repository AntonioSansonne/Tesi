import matplotlib.pyplot as plt

# Creazione figura
fig, ax = plt.subplots()

# Disegno strade
ax.plot([0, 1], [0, 0], 'k-')
ax.plot([0, 0], [0, 1], 'k-')

# Posizione veicoli
ax.plot([0.5], [0.1], 'bo')  # Veicolo 1
ax.plot([0.1], [0.5], 'ro')  # Veicolo 2

# Annotazioni
ax.text(0.5, 0.12, 'Veicolo 1', ha='center')
ax.text(0.12, 0.5, 'Veicolo 2', ha='center')

plt.axis('equal')
plt.axis('off')
plt.show()



import json
import matplotlib.pyplot as plt
import numpy as np

# Carica i dati JSON dal file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Estrai informazioni rilevanti dal JSON
def extract_intersection_info(json_data):
    location = json_data["location"]
    street_names = json_data["toponomy"]["streetNames"]
    street_count = json_data["parameters"]["streetCount"]
    has_traffic_lights = json_data["parameters"]["trafficLights"]
    return location, street_names, street_count, has_traffic_lights

# Esempio di uso
file_path = '../jsonFile/auto1.json'
json_data = load_json_data(file_path)
location, street_names, street_count, has_traffic_lights = extract_intersection_info(json_data)

print(location, street_names, street_count, has_traffic_lights)


def draw_intersection(street_names, street_count, has_traffic_lights):
    fig, ax = plt.subplots()

    # Disegna le strade come linee
    for i in range(street_count):
        angle = np.pi * 2 / street_count * i
        x = np.cos(angle)
        y = np.sin(angle)
        ax.plot([0, x], [0, y], 'k-')

    # Aggiungi dettagli (es. semafori)
    if has_traffic_lights:
        ax.plot(0.1, 0.1, 'go')  # Esempio: disegna un semaforo come punto verde

    # Imposta limiti e titolo del grafico
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_title('Incrocio')
    plt.axis('off')

    # Mostra il grafico
    plt.show()


draw_intersection(street_names, street_count, has_traffic_lights)
