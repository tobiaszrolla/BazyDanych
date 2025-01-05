// Funkcja do przekierowania na stronę dodawania lub usuwania zajęć
function navigateToZajecia(action) {
    if (action === 'dodaj') {
        window.location.href = "dodaj_zajecia.html"; // Przekierowanie na stronę dodawania zajęć
    } else if (action === 'usun') {
        window.location.href = "usun_zajecia.html"; // Przekierowanie na stronę usuwania zajęć
    }
}
