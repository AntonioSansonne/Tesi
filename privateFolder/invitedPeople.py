import json


def leggi_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def scrivi_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def inserisci_dati():
    name = input("Inserisci il nome della persona: ")
    surname = input("Inserisci il cognome della persona: ")
    city = input("Inserisci la città di provenienza: ")
    invited = input("La persona è invitata? (true/false): ").lower() == 'true'
    phoneNumber = input("Inserisci il numero di telefono della persona: ")

    # Nuova struttura aggiornata del JSON
    willBe = input("La persona sarà presente? (true/false): ").lower() == 'true'
    willKnow = input("La persona farà sapere se sarà presente? (true/false): ").lower() == 'true'
    intolerances = input("Inserisci eventuali intolleranze (separate da virgola): ").split(',')
    allergies = input("Inserisci eventuali allergie (separate da virgola): ").split(',')

    isAlone = input("La persona sarà da sola? (true/false): ").lower() == 'true'
    isSelfEmployed = input("La persona è autonoma? (true/false): ").lower() == 'true'
    searchRide = input("La persona cerca un passaggio? (true/false): ").lower() == 'true'

    new_person = {
        "people": {
            "name": name,
            "surname": surname
        },
        "city": {
            "from": city,
            "invited": invited
        },
        "contact": {
            "phoneNumber": phoneNumber
        },
        "info": {
            "willBe": willBe,
            "willKnow": willKnow,
            "intolerances": intolerances,
            "allergies": allergies
        },
        "knowReach": {
            "isAlone": isAlone,
            "isSelfEmployed": isSelfEmployed,
            "searchRide": searchRide
        }
    }

    return new_person


def cerca_utente(utenti, nome, cognome):
    for utente in utenti:
        if utente['people']['name'] == nome and utente['people']['surname'] == cognome:
            return utente
    return None


def crea_utente():
    existing_data = leggi_json("people.json")
    new_data = inserisci_dati()

    # Controllo unicità del numero di telefono
    for persona in existing_data:
        if persona['contact']['phoneNumber'] == new_data['contact']['phoneNumber']:
            print("Errore: Il numero di telefono è già stato inserito.")
            return

    existing_data.append(new_data)
    scrivi_json("people.json", existing_data)
    print("Utente inserito con successo.")


def modifica_utente():
    existing_data = leggi_json("people.json")
    nome = input("Inserisci il nome della persona da modificare: ")
    cognome = input("Inserisci il cognome della persona da modificare: ")
    utente = cerca_utente(existing_data, nome, cognome)
    if utente:
        # Modifiche dei dati dell'utente
        # Questa parte dipende da cosa si vuole modificare

        # Sovrascrivi solo i dati dell'utente modificato
        utente['people']['name'] = input("Nuovo nome: ")
        utente['people']['surname'] = input("Nuovo cognome: ")
        utente['city']['from'] = input("Nuova città di provenienza: ")
        utente['city']['invited'] = input("La persona è invitata? (true/false): ").lower() == 'true'
        utente['contact']['phoneNumber'] = input("Nuovo numero di telefono: ")
        utente['info']['willBe'] = input("La persona sarà presente? (true/false): ").lower() == 'true'
        utente['info']['willKnow'] = input("La persona farà sapere se sarà presente? (true/false): ").lower() == 'true'
        utente['info']['intolerances'] = input("Nuove intolleranze (separate da virgola): ").split(',')
        utente['info']['allergies'] = input("Nuove allergie (separate da virgola): ").split(',')
        utente['knowReach']['isAlone'] = input("La persona sarà da sola? (true/false): ").lower() == 'true'
        utente['knowReach']['isSelfEmployed'] = input("La persona è autonoma? (true/false): ").lower() == 'true'
        utente['knowReach']['searchRide'] = input("La persona cerca un passaggio? (true/false): ").lower() == 'true'

        # Aggiorna il file JSON solo con i dati dell'utente modificato
        scrivi_json("people.json", existing_data)
        print("Utente modificato con successo.")
    else:
        print("Utente non trovato.")
def elimina_utente():
    existing_data = leggi_json("people.json")
    nome = input("Inserisci il nome della persona da eliminare: ")
    cognome = input("Inserisci il cognome della persona da eliminare: ")
    utente = cerca_utente(existing_data, nome, cognome)
    if utente:
        existing_data.remove(utente)
        scrivi_json("people.json", existing_data)
        print("Utente eliminato con successo.")
    else:
        print("Utente non trovato.")


def stampa_utenti():
    existing_data = leggi_json("people.json")
    for utente in existing_data:
        name = utente['people']['name']
        surname = utente['people']['surname']
        willBe = "Presente" if utente['info']['willBe'] else "Non presente"
        willKnow = "Darà conferma" if utente['info']['willKnow'] else "Deve ancora confermare"
        print(f"Nome: {name} - Cognome: {surname}\nSarà presente: {willBe}\nConferma presenza: {willKnow}")


def main():
    while True:
        print("\n1. Inserisci nuovo utente")
        print("2. Modifica utente")
        print("3. Elimina utente")
        print("4. Stampare tutti gli utenti")
        print("5. Esci")
        scelta = input("Scelta: ")

        if scelta == "1":
            crea_utente()
        elif scelta == "2":
            modifica_utente()
        elif scelta == "3":
            elimina_utente()
        elif scelta == "4":
            stampa_utenti()
        elif scelta == "5":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()
