document.getElementById("addRoomForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Zapobiega domyślnej akcji formularza

    // Zbieranie danych z formularza
    const nazwa = document.getElementById("nazwa").value;
    const capacity = document.getElementById("capacity").value;
    const availability = document.getElementById("availability").value === "True"; // Przekształcenie na wartość boolean

    // Tworzenie obiektu z danymi do wysłania
    const roomData = {
        nazwa: nazwa,
        capacity: capacity,
        availability: availability
    };

    // Wysyłanie żądania POST do API
    fetch("/add_room/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')  // Pobieranie CSRF tokenu
        },
        body: JSON.stringify(roomData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("responseMessage").innerHTML = data.message;
            document.getElementById("responseMessage").style.color = "green";
        } else if (data.error) {
            document.getElementById("responseMessage").innerHTML = data.error;
            document.getElementById("responseMessage").style.color = "red";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("responseMessage").innerHTML = "Wystąpił błąd podczas dodawania sali.";
        document.getElementById("responseMessage").style.color = "red";
    });
});

// Funkcja do pobierania CSRF tokenu z cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].split("=");
            if (cookie[0] === name) {
                cookieValue = decodeURIComponent(cookie[1]);
                break;
            }
        }
    }
    return cookieValue;
}
