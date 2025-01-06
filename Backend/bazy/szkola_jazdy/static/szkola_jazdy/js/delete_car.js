document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("deleteCarForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const registrationNumber = document.getElementById("registrationNumber").value;

        try {
            const response = await fetch(`/delete_car/${registrationNumber}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Pobierz CSRF token
                    "Content-Type": "application/json",
                },
            });

            const data = await response.json();
            responseMessage.textContent = data.message || data.error;

            responseMessage.style.color = response.ok ? "green" : "red";
        } catch (error) {
            responseMessage.textContent = "Wystąpił błąd podczas usuwania samochodu.";
            responseMessage.style.color = "red";
        }
    });
});

// Funkcja do pobierania CSRF tokena
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
