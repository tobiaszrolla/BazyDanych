// Obsługa przycisków do wyświetlania formularzy
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

    addRow("teoretyczne-tabela", [data, godzinaRozpoczęcia, godzinaZakończenia, sala, kategoria]);
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

    addRow("praktyczne-tabela", [data, godzinaRozpoczęcia, godzinaZakończenia, rejestracja, kategoria]);
    toggleForm("praktyczne-form");
});

// Funkcja do dodawania wierszy do tabeli
function addRow(tableId, rowData) {
    const table = document.getElementById(tableId);
    const row = table.insertRow();

    rowData.forEach((cellData) => {
        const cell = row.insertCell();
        cell.textContent = cellData;
    });
}
