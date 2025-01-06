document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("modifyUserForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Zapobiega przeładowaniu strony

        const email = document.getElementById("email").value;
        const requestData = {
            imię: document.getElementById("imię").value || undefined,
            nazwisko: document.getElementById("nazwisko").value || undefined,
            nrTelefonu: document.getElementById("nrTelefonu").value || undefined,
            data_urodzenia: document.getElementById("data_urodzenia").value || undefined,
            typ_użytkownika: document.getElementById("typ_użytkownika").value || undefined,
            password: document.getElementById("password").value || undefined,
        };

        // Usuwanie pustych wartości
        Object.keys(requestData).forEach(
            (key) => requestData[key] === undefined && delete requestData[key]
        );

        try {
            const response = await fetch(`/modify_user/${email}/`, {
                method: "PUT",
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
