import hashlib

def custom_intersection_hash(intersection_data):
    # Unisci i dati dell'incrocio in una stringa
    intersection_str = "|".join(sorted(intersection_data))

    # Usa una funzione di hash, ad esempio SHA-256
    hash_object = hashlib.sha256(intersection_str.encode())

    # Ottieni il "fingerprint" unico come valore esadecimale
    fingerprint = hash_object.hexdigest()
    print("Fingerprint: " + fingerprint)
    return fingerprint

custom_intersection_hash("Via Calò")
custom_intersection_hash("Via Calo")
custom_intersection_hash("Via Calo'")


def custom_intersection_hash_norm(intersection_data):
    # Normalizza i dati dell'incrocio (rimuovi spazi e caratteri speciali)
    normalized_intersection = intersection_data.lower().replace(" ", "").replace("'", "")

    # Usa una funzione di hash, ad esempio SHA-256
    hash_object = hashlib.sha256(normalized_intersection.encode())

    # Ottieni il "fingerprint" unico come valore esadecimale
    fingerprint = hash_object.hexdigest()
    print("Fingerprint norm: " + fingerprint)
    return fingerprint

custom_intersection_hash_norm("Via Calò")
custom_intersection_hash_norm("Via Calo")
custom_intersection_hash_norm("Via Calo'")
