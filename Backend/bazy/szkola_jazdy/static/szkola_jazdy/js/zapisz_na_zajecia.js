document.addEventListener("DOMContentLoaded", function() {
    // Funkcja do pobrania dostępnych zajęć
    function fetchAvailableClasses() {
        fetch('/dostępne_zajęcia/')
            .then(response => response.json())
            .then(data => {
                const availableClassesDiv = document.getElementById("availableClasses");
                availableClassesDiv.innerHTML = ''; // Wyczyść poprzednią listę

                // Dodanie zajęć do strony
                data.forEach(zajęcia => {
                    const classElement = document.createElement('div');
                    classElement.classList.add('class-item');
                    classElement.innerHTML = `
                        <h3>${zajęcia.title}</h3>
                        <p><strong>Data:</strong> ${zajęcia.data}</p>
                        <p><strong>Godzina:</strong> ${zajęcia.start} - ${zajęcia.end}</p>
                        <p><strong>Wolne miejsca:</strong> ${zajęcia.wolne_miejsca}</p>
                        <button class="zapisz-btn" data-zajecia-id="${zajęcia.id}">Zapisz się</button>
                    `;
                    availableClassesDiv.appendChild(classElement);
                });

                // Dodanie nasłuchiwaczy na przyciski zapisu
                document.querySelectorAll('.zapisz-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const zajęciaId = this.getAttribute('data-zajecia-id');
                        zapiszzajecia(zajęciaId);
                    });
                });
            })
            .catch(error => {
                console.error('Błąd przy pobieraniu dostępnych zajęć:', error);
            });
    }

    // Funkcja do zapisania na zajęcia
    function zapiszzajecia(zajęciaId) {
        fetch(`/zapiszzajecia/${zajęciaId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            const confirmationMessage = document.getElementById("confirmationMessage");
            const confirmationText = document.getElementById("confirmationText");

            if (data.error) {
                confirmationText.innerText = "Błąd: " + data.error;
            } else {
                confirmationText.innerText = data.message;
            }

            confirmationMessage.style.display = 'block';
        })
        .catch(error => {
            console.error('Błąd przy zapisie na zajęcia:', error);
        });
    }

    // Załaduj dostępne zajęcia
    fetchAvailableClasses();
});
