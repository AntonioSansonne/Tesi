document.addEventListener('DOMContentLoaded', function () {
    loadUsers(); // Carica gli utenti all'avvio

    const userForm = document.getElementById('userForm');
    userForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Raccogli i dati dal form
        const formData = new FormData(userForm);
        const userData = Object.fromEntries(formData.entries());
        const updateMode = document.getElementById('updateMode').value === 'true';

        if (updateMode) {
            const phoneNumber = document.getElementById('updatingPhoneNumber').value;
            updateUser(phoneNumber, userData); // Aggiorna l'utente esistente
        } else {
            createUser(userData); // Crea un nuovo utente
        }
    });
});

function loadUsers() {
    fetch('/get_users')
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('usersList');
            usersList.innerHTML = ''; // Pulisce la lista attuale
            data.forEach(user => {
                const userItem = document.createElement('li');
                userItem.textContent = user;
                usersList.appendChild(userItem);
            });
        })
        .catch(error => console.error('Error:', error));
}

function createUser(userData) {
    // Invia i dati al server tramite POST
    fetch('/save_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Utente salvato con successo!');
            loadUsers(); // Ricarica la lista degli utenti dopo il salvataggio
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Si è verificato un errore!');
        });
}

function updateUser(phoneNumber, userData) {
    fetch(`/update_user/${phoneNumber}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Utente aggiornato con successo!');
            loadUsers(); // Ricarica la lista degli utenti dopo l'aggiornamento
        })
        .catch(error => console.error('Error:', error));
}

function deleteUser(phoneNumber) {
    fetch(`/delete_user/${phoneNumber}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Utente eliminato con successo!');
            loadUsers(); // Ricarica la lista degli utenti dopo la cancellazione
        })
        .catch(error => console.error('Error:', error));
}