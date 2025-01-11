document.getElementById("dodaj-teoretyczne").addEventListener("click", () => {
    toggleForm("teoretyczne-form");
});

document.getElementById("dodaj-praktyczne").addEventListener("click", () => {
    toggleForm("praktyczne-form");
});

// Funkcja do przełączania widoczności formularzy
function toggleForm(formId) {
    const form = document.getElementById(formId);
    form.classList.toggle("hidden");
}

// Obsługa formularza teoretycznego
document.getElementById("teoretyczne-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const data = document.getElementById("teoretyczne-data").value;
    const godzinaRozpoczęcia = document.getElementById("teoretyczne-godzina-rozpoczęcia").value;
    const godzinaZakończenia = document.getElementById("teoretyczne-godzina-zakończenia").value;
    const sala = document.getElementById("teoretyczne-sala").value;
    const kategoria = document.getElementById("teoretyczne-kategoria").value;

    const zajeciaData = {
        data,
        godzina_rozpoczęcia: godzinaRozpoczęcia,
        godzina_zakończenia: godzinaZakończenia,
        nazwa_sali: sala,
        kategoria: kategoria
    };
    // Wysyłanie danych do serwera
    sendZajęciaData(zajeciaData, "teoretyczne-tabela");

    // Dodawanie wiersza do tabeli (lokalne przechowywanie)
    addRow("teoretyczne-tabela", [data, godzinaRozpoczęcia, godzinaZakończenia, sala, kategoria]);

    // Ukrywanie formularza
    toggleForm("teoretyczne-form");
});

// Obsługa formularza praktycznego
document.getElementById("praktyczne-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const data = document.getElementById("praktyczne-data").value;
    const godzinaRozpoczęcia = document.getElementById("praktyczne-godzina-rozpoczęcia").value;
    const godzinaZakończenia = document.getElementById("praktyczne-godzina-zakończenia").value;
    const rejestracja = document.getElementById("praktyczne-rejestracja").value;
    const kategoria = document.getElementById("praktyczne-kategoria").value;


    const zajeciaData = {
        data,
        godzina_rozpoczęcia: godzinaRozpoczęcia,
        godzina_zakończenia: godzinaZakończenia,
        numer_rejestracyjny: rejestracja,
        kategoria: kategoria
    };

    // Wysyłanie danych do serwera
    sendZajęciaData(zajeciaData, "praktyczne-tabela");

    // Dodawanie wiersza do tabeli (lokalne przechowywanie)
    addRow("praktyczne-tabela", [data, godzinaRozpoczęcia, godzinaZakończenia, rejestracja, kategoria]);

    // Ukrywanie formularza
    toggleForm("praktyczne-form");
});

// Funkcja do wysyłania danych do widoku Django
function sendZajęciaData(data, tableId) {
    fetch("/add_zajęcia/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // Wysyłanie ciasteczka z danymi
            "X-CustomCookie": getCookie("myCustomCookie"),  // Tutaj zmieniłem na twoje ciasteczko
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then((errorData) => {
                    throw new Error(errorData.error || "Wystąpił problem podczas zapisywania zajęć.");
                });
            }
        })
        .then((responseData) => {
            alert(responseData.message || "Zajęcia zostały dodane pomyślnie!");
            addRow(tableId, Object.values(data));
        })
        .catch((error) => {
            console.error(error);
            alert(error.message);
        });
}

// Funkcja do dodawania wierszy do tabeli
function addRow(tableId, rowData) {
    const table = document.getElementById(tableId);
    const row = table.insertRow();

    rowData.forEach((cellData) => {
        const cell = row.insertCell();
        cell.textContent = cellData;
    });
}

// Funkcja do pobierania ciasteczka (zwykłe ciastka, nie CSRF token)
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
