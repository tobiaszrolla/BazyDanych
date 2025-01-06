// Funkcja obsługująca usuwanie zajęć
document.getElementById('deleteZajeciaForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Zapobiega domyślnemu odświeżeniu strony

    const zajeciaId = document.getElementById('zajeciaId').value;
    const responseMessage = document.getElementById('responseMessage');

    // Wysłanie żądania DELETE do serwera
    try {
        const response = await fetch(`/delete_zajęcia/${zajeciaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken(), // Dodanie tokena CSRF
                'Content-Type': 'application/json',
            },
        });

        const result = await response.json();

        // Wyświetlenie wiadomości zwrotnej od serwera
        if (response.ok) {
            responseMessage.textContent = result.message;
            responseMessage.style.color = "green";
        } else {
            responseMessage.textContent = result.error || "Wystąpił błąd.";
            responseMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Błąd podczas usuwania zajęć:", error);
        responseMessage.textContent = "Wystąpił błąd podczas komunikacji z serwerem.";
        responseMessage.style.color = "red";
    }
});

// Funkcja do pobierania tokena CSRF z ciasteczek
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}
