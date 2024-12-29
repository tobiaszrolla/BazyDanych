document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutButton");
    const enrollButton = document.getElementById("enrollButton");
    const calendarButton = document.getElementById("calendarButton");
    const reviewsButton = document.getElementById("reviewsButton");
    const bookClassButton = document.getElementById("bookClassButton");
    const greetingMessage = document.getElementById("greetingMessage");

    // Funkcja do ustawiania przywitania
    function setGreeting() {
        const currentHour = new Date().getHours();
        let greeting = "";

        if (currentHour < 12) {
            greeting = "Dzień dobry";
        } else if (currentHour < 18) {
            greeting = "Dzień dobry";
        } else {
            greeting = "Dobry wieczór";
        }

        greetingMessage.textContent = `${greeting}, użytkowniku!`; // Przykładowe przywitanie
    }

    // Ustawienie przywitania po załadowaniu strony
    setGreeting();

    // Obsługa wylogowania
    logoutButton.addEventListener("click", async (event) => {
        event.preventDefault();
        try {
            const response = await fetch("/logout/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                },
            });

            if (response.ok) {
                window.location.href = '/login';  // Po wylogowaniu przekierowanie na stronę logowania
            } else {
                alert("Wystąpił błąd podczas wylogowania.");
            }
        } catch (error) {
            console.error("Błąd wylogowania:", error);
        }
    });

    // Funkcje do obsługi innych przycisków
    enrollButton.addEventListener("click", () => {
        window.location.href = '/kursy/zapis';  // Przekierowanie do strony zapisu na kurs
    });

    calendarButton.addEventListener("click", () => {
        window.location.href = '/kalendarz';  // Przekierowanie do kalendarza zajęć
    });

    reviewsButton.addEventListener("click", () => {
        window.location.href = '/opinie';  // Przekierowanie do sekcji z opiniami
    });

    bookClassButton.addEventListener("click", () => {
        window.location.href = '/zajecia/zapis';  // Przekierowanie do zapisu na zajęcia
    });

    // Funkcja do pobierania tokena CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }
});
