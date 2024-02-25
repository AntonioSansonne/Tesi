import osmpy

# Apre il file OSM
osm_data = osmpy.parse_file("mappa.osm")

# Esempio: Visualizza il numero di nodi nella mappa
print("Numero di nodi nella mappa:", len(osm_data.nodes))
