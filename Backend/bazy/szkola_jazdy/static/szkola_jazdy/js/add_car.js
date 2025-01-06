document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addCarForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Zapobiega przeładowaniu strony

        const registrationNumber = document.getElementById("registration_number").value;
        const model = document.getElementById("model").value;
        const productionYear = document.getElementById("production_year").value;
        const availability = document.getElementById("availability").value;

        const requestData = {
            registration_number: registrationNumber,
            model: model,
            production_year: productionYear,
            availability: availability === "true",
        };

        try {
            const response = await fetch("/add_car/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), // Pobiera CSRF token
                },
                body: JSON.stringify(requestData),
            });

            const result = await response.json();

            if (response.ok) {
                // Sukces
                responseMessage.textContent = result.message;
                responseMessage.className = "success-message";
                form.reset(); // Reset formularza
            } else {
                // Błąd
                responseMessage.textContent = result.error || "Wystąpił nieznany błąd.";
                responseMessage.className = "error-message";
            }
        } catch (error) {
            responseMessage.textContent = "Wystąpił błąd podczas wysyłania żądania.";
            responseMessage.className = "error-message";
            console.error("Error:", error);
        }

        responseMessage.classList.remove("hidden");
    });

    // Funkcja do pobierania CSRF tokenu
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
