/*
document.getElementById("modifyRoomForm").addEventListener("submit", function (event) {
    event.preventDefault();

    // Pobranie wartości z formularza
    const availability = document.getElementById("availability").value === "true";
    const capacity = parseInt(document.getElementById("capacity").value, 10);

    // Pobranie nazwy sali z URL (dynamiczne przekierowanie)
    const roomName = window.location.pathname.split("/")[2];

    // Wysłanie żądania PUT
    fetch(`/modify_room/${roomName}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            availability: availability,
            capacity: capacity,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const messageDiv = document.getElementById("responseMessage");
            if (data.error) {
                messageDiv.textContent = `Błąd: ${data.error}`;
                messageDiv.style.color = "red";
            } else {
                messageDiv.textContent = data.message;
                messageDiv.style.color = "green";
            }
        })
        .catch((error) => {
            console.error("Wystąpił błąd:", error);
        });
});

// Funkcja do pobierania CSRF tokena
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
 */
// Funkcja do pobierania CSRF tokena z plików cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.getElementById("modifyRoomForm").addEventListener("submit", function (event) {
    event.preventDefault();

    // Pobranie wartości z formularza
    const nazwa = document.getElementById("nazwa").value;
    const availability = document.getElementById("availability").value === "true";
    const capacity = parseInt(document.getElementById("capacity").value, 10);

    // Pobranie nazwy sali z URL (dynamiczne przekierowanie)
    const roomName = window.location.pathname.split("/")[2];

    // Wysłanie żądania PUT
    fetch(`/modify_room/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            nazwa: nazwa,
            availability: availability,
            capacity: capacity,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const messageDiv = document.getElementById("responseMessage");
            if (data.error) {
                messageDiv.textContent = `Błąd: ${data.error}`;
                messageDiv.style.color = "red";
            } else {
                messageDiv.textContent = data.message;
                messageDiv.style.color = "green";
            }
        })
        .catch((error) => {
            console.error("Wystąpił błąd:", error);
        });
});