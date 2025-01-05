document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("zapisForm");
    const responseMessage = document.getElementById("responseMessage");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const kategoria = document.getElementById("kategoria").value;
        const lekcjeTeoretyczne = parseInt(document.getElementById("lekcjeTeoretyczne").value) || 0;
        const lekcjePraktyczne = parseInt(document.getElementById("lekcjePraktyczne").value) || 0;

        try {
            const csrfToken = getCSRFToken(); // Pobierz token CSRF
            const response = await fetch("/zapisz_na_kurs/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    kategoria,
                    lekcje_teoretyczne: lekcjeTeoretyczne,
                    lekcje_praktyczne: lekcjePraktyczne,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                responseMessage.textContent = data.message;
                responseMessage.className = "success";
            } else {
                responseMessage.textContent = data.error || "Wystąpił błąd.";
                responseMessage.className = "error";
            }
        } catch (error) {
            responseMessage.textContent = "Wystąpił błąd po stronie klienta.";
            responseMessage.className = "error";
            console.error("Błąd:", error);
        } finally {
            responseMessage.classList.remove("hidden");
        }
    });

    // Pobranie tokena CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }
});
