document.getElementById('deleteRoomForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const nazwa = document.getElementById('nazwa').value;
    const url = `/delete_room/${nazwa}/`;

    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Dodajemy token CSRF
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('responseMessage').textContent = data.message || data.error;
    })
    .catch(error => {
        document.getElementById('responseMessage').textContent = 'Wystąpił błąd.';
    });
});

// Funkcja do pobierania tokenu CSRF z cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
