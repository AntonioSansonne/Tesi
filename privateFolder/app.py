from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)


def is_valid_phone_number(phonenumber):
    """Valida il formato del numero di telefono."""
    pattern = re.compile(r"^\+?[0-9]{10,15}$")
    return pattern.match(phonenumber)


def sanitize_string(input_string):
    """Rimuove caratteri non desiderati dalle stringhe."""
    return re.sub(r'[^\w\s]', '', input_string)


def sanitize_boolean(input_value):
    """Converte una stringa in un valore booleano."""
    if isinstance(input_value, str):
        return input_value.lower() in ["true", "1", "t", "y", "yes"]
    return bool(input_value)


def sanitize_list_string(input_list):
    """Sanifica una lista di stringhe."""
    return [sanitize_string(item) for item in input_list if isinstance(item, str)]


def validate_user_data(user_data):
    """Aggiornata per includere nuove validazioni e sanificazioni."""
    # Validazione del numero di telefono
    if not is_valid_phone_number(user_data.get('contact', {}).get('phoneNumber', '')):
        return False, "Numero di telefono non valido."

    # Sanificazioni
    user_data['people']['name'] = sanitize_string(user_data['people']['name'])
    user_data['people']['surname'] = sanitize_string(user_data['people']['surname'])
    user_data['city']['from'] = sanitize_string(user_data['city']['from'])
    user_data['city']['invited'] = sanitize_boolean(user_data['city']['invited'])
    user_data['info']['willBe'] = sanitize_boolean(user_data['info']['willBe'])
    user_data['info']['willKnow'] = sanitize_boolean(user_data['info']['willKnow'])
    user_data['info']['intolerances'] = sanitize_list_string(user_data['info']['intolerances'])
    user_data['info']['allergies'] = sanitize_list_string(user_data['info']['allergies'])
    user_data['knowReach']['isAlone'] = sanitize_boolean(user_data['knowReach']['isAlone'])
    user_data['knowReach']['isSelfEmployed'] = sanitize_boolean(user_data['knowReach']['isSelfEmployed'])
    user_data['knowReach']['searchRide'] = sanitize_boolean(user_data['knowReach']['searchRide'])

    # Aggiungi altre validazioni specifiche per il tuo caso d'uso qui

    return True, "Dati validi."


def leggi_json(file_path):
    if not os.path.exists(file_path):
        return []  # Restituisce una lista vuota se il file non esiste
    with open(file_path, 'r') as file:
        return json.load(file)


def scrivi_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


@app.route('/save_user', methods=['POST'])
def save_user():
    user_data = request.json
    is_valid, message = validate_user_data(user_data)
    if not is_valid:
        return jsonify({"error": message}), 400
    try:
        existing_data = leggi_json("people.json")
        # Verifica l'unicità del numero di telefono
        if any(persona['contact']['phoneNumber'] == user_data['phoneNumber'] for persona in existing_data):
            return jsonify({"error": "Il numero di telefono è già stato inserito."}), 400

        existing_data.append(user_data)  # Aggiunge il nuovo utente
        scrivi_json("people.json", existing_data)
        return jsonify({"message": "Utente salvato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_user/<phoneNumber>', methods=['PUT'])
def update_user(phonenumber):
    update_data = request.json
    try:
        existing_data = leggi_json("people.json")
        user_found = False
        for i, user in enumerate(existing_data):
            if user['contact']['phoneNumber'] == phonenumber:
                existing_data[i] = update_data  # Aggiorna l'utente con i nuovi dati
                user_found = True
                break
        if not user_found:
            return jsonify({"error": "Utente non trovato."}), 404
        scrivi_json("people.json", existing_data)
        return jsonify({"message": "Utente aggiornato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_user/<phoneNumber>', methods=['DELETE'])
def delete_user(phonenumber):
    try:
        existing_data = leggi_json("people.json")
        new_data = [user for user in existing_data if user['contact']['phoneNumber'] != phonenumber]
        if len(existing_data) == len(new_data):
            return jsonify({"error": "Utente non trovato."}), 404
        scrivi_json("people.json", new_data)
        return jsonify({"message": "Utente eliminato con successo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        existing_data = leggi_json("people.json")
        users_formatted = []
        for user in existing_data:
            name = user['people']['name']
            surname = user['people']['surname']
            phonenumber = user['contact']['phoneNumber']
            willbe = "Sarà presente" if user['info']['willBe'] else "Non sarà presente"
            willknow = "Darà conferma" if user['info']['willKnow'] else "Non darà conferma"
            user_str = f"{name} {surname} {phonenumber} {willbe} {willknow}"
            users_formatted.append(user_str)
        return jsonify(users_formatted), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
