
// Funkcja do pobierania CSRF tokena z plików cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Sprawdzenie, czy ten cookie zawiera nazwę
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.getElementById("modifyCarForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Pobranie danych z formularza
    const registrationNumber = document.getElementById("registration_number").value;
    const model = document.getElementById("model").value;
    const productionYear = document.getElementById("production_year").value;
    const availability = document.getElementById("availability").value === "true";

    // Sprawdzenie, czy numer rejestracyjny został podany
    if (!registrationNumber) {
        alert("Numer rejestracyjny jest wymagany.");
        return;
    }

    try {
        // Wysłanie żądania PUT
        const response = await fetch(`/modify_car/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken') // Pobranie CSRF tokena
            },
            body: JSON.stringify({
                registration_number: registrationNumber,
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
