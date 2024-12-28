document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const registerButton = document.getElementById("registerButton");

    // Dodanie miejsca na wiadomości
    const messageDiv = document.createElement("div");
    messageDiv.id = "message";
    form.appendChild(messageDiv);

    // Obsługa kliknięcia przycisku rejestracji
    registerButton.addEventListener("click", async (event) => {
        event.preventDefault(); // Zapobieganie domyślnemu zachowaniu formularza

        // Pobranie danych z formularza
        const formData = {
            email: form.email.value.trim(),
            nrTelefonu: form.nrTelefonu.value.trim(),
            imię: form.imię.value.trim(),
            nazwisko: form.nazwisko.value.trim(),
            data_urodzenia: form.data_urodzenia.value.trim(),
            typ_użytkownika: form.typ_użytkownika.value.trim(),
            password: form.password.value.trim(),
        };

        // Walidacja: Sprawdzanie, czy wszystkie pola są wypełnione
        for (const [key, value] of Object.entries(formData)) {
            if (!value) {
                messageDiv.textContent = `Pole "${key}" jest wymagane.`;
                messageDiv.style.color = "red";
                return;
            }
        }

        // Wysłanie żądania do API
        try {
            const response = await fetch("/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            // Wyświetlenie odpowiedzi
            if (response.ok) {
                messageDiv.textContent = data.message;
                messageDiv.style.color = "green";
                form.reset(); // Resetowanie formularza po sukcesie
            } else {
                messageDiv.textContent = data.error;
                messageDiv.style.color = "red";
            }
        } catch (error) {
            messageDiv.textContent = "Wystąpił błąd podczas rejestracji.";
            messageDiv.style.color = "red";
            console.error(error);
        }
    });

    // Funkcja do pobierania tokena CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : "";
    }
});
