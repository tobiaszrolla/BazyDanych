function deleteUser() {
    const email = document.getElementById('email').value;
    if (!email) {
        alert('Proszę podać e-mail użytkownika!');
        return;
    }

    if (confirm(`Czy na pewno chcesz usunąć użytkownika o adresie e-mail: ${email}?`)) {
        fetch(`/delete_user/${email}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), // Pobierz token CSRF
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message); // Wyświetlenie komunikatu o sukcesie
            } else {
                alert('Wystąpił błąd: ' + data.error); // Obsługa błędu
            }
        })
        .catch(error => {
            console.error('Błąd:', error);
            alert('Wystąpił błąd podczas usuwania użytkownika.');
        });
    }
}

// Funkcja do pobierania tokena CSRF
function getCsrfToken() {
    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
}
