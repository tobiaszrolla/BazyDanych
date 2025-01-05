document.addEventListener('DOMContentLoaded', () => {
    const opiniaForm = document.getElementById('opiniaForm');
    const responseMessage = document.getElementById('responseMessage');
    const opinieList = document.getElementById('opinieList');

    // Funkcja do załadowania opinii
    async function loadOpinie() {
        try {
            const response = await fetch('/pobierz_opinie/');
            const data = await response.json();

            if (response.ok) {
                opinieList.innerHTML = ''; // Wyczyść istniejące opinie
                data.opinie.forEach(opinia => {
                    const opiniaItem = document.createElement('li');
                    opiniaItem.textContent = opinia;
                    opinieList.appendChild(opiniaItem);
                });
            } else {
                displayMessage('Nie udało się załadować opinii.', 'error');
            }
        } catch (error) {
            displayMessage('Wystąpił błąd podczas ładowania opinii.', 'error');
        }
    }

    opiniaForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const opinia = document.getElementById('opinia').value.trim();
        const csrfToken = getCookie('csrftoken');

        if (!opinia) {
            displayMessage('Proszę wpisać opinię.', 'error');
            return;
        }

        try {
            const response = await fetch('/dodaj_opinie/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ opinia: opinia }),
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(data.message, 'success');
                opiniaForm.reset();
                await loadOpinie(); // Odśwież opinie po dodaniu nowej
            } else {
                const errors = data.errors || { message: data.message };
                displayMessage(Object.values(errors).join('<br>'), 'error');
            }
        } catch (error) {
            displayMessage('Wystąpił błąd podczas zapisywania opinii.', 'error');
        }
    });

    function displayMessage(message, type) {
        responseMessage.style.display = 'block';
        responseMessage.style.color = type === 'success' ? 'green' : 'red';
        responseMessage.innerHTML = message;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Załaduj opinie na początku
    loadOpinie();
});
