document.getElementById("modifyCarForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Pobranie danych z formularza
    const model = document.getElementById("model").value;
    const productionYear = document.getElementById("production_year").value;
    const availability = document.getElementById("availability").value === "true";

    // Pobranie numeru rejestracyjnego z URL
    const urlParts = window.location.pathname.split('/');
    const registrationNumber = urlParts[urlParts.length - 2]; // np. /modify_car/<registration_number>/

    try {
        // Wysłanie żądania PUT
        const response = await fetch(`/modify_car/${registrationNumber}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken') // Pobranie CSRF tokena
            },
            body: JSON.stringify({
                model: model,
                production_year: productionYear,
                availability: availability
            })
        });

        const data = await response.json();
        const messageElement = document.getElementById("message");

        if (response.ok) {
            messageElement.textContent = data.message;
            messageElement.style.color = "green";
        } else {
            messageElement.textContent = data.error;
            messageElement.style.color = "red";
        }
    } catch (error) {
        console.error("Wystąpił błąd:", error);
    }
});

// Funkcja do pobierania CSRF tokena
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
