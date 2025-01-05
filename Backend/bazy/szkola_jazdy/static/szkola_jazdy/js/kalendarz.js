document.addEventListener("DOMContentLoaded", () => {
    const reloadButton = document.getElementById("reloadButton");
    const zajeciaTableBody = document.getElementById("zajeciaTableBody");

    // Funkcja do pobierania danych z API
    async function loadZajecia() {
        try {
            const response = await fetch("/kalendarz/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(), // Funkcja pobierająca token CSRF
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                alert(`Błąd: ${data.error}`);
                return;
            }

            updateTable(data.zajęcia);
        } catch (error) {
            console.error("Wystąpił błąd podczas ładowania danych:", error);
        }
    }

    // Funkcja do aktualizowania tabeli zajęć
    function updateTable(zajecia) {
        zajeciaTableBody.innerHTML = ""; // Wyczyść tabelę

        zajecia.forEach((zajecie) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${zajecie.data || "-"}</td>
                <td>${zajecie.godzina_rozpoczęcia || "-"}</td>
                <td>${zajecie.godzina_zakończenia || "-"}</td>
                <td>${zajecie.sala || "-"}</td>
                <td>${zajecie.samochód || "-"}</td>
                <td>${zajecie.instruktor || "-"}</td>
            `;

            zajeciaTableBody.appendChild(row);
        });
    }

    // Funkcja pobierająca token CSRF z ciasteczek
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find((row) => row.startsWith("csrftoken="))
            ?.split("=")[1];
        return cookieValue || "";
    }

    // Przycisk odświeżania
    reloadButton.addEventListener("click", loadZajecia);

    // Automatyczne ładowanie zajęć przy starcie
    loadZajecia();
});
