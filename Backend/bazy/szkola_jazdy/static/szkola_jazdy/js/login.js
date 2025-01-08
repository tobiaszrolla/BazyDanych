document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Check if email and password are provided
    if (!email || !password) {
        alert("Email i hasło są wymagane.");
        return;
    }

    const data = {
        email: email,
        password: password
    };

    // Send login request to the Django backend
    fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Display error message if any
        } else if (data.message) {
            alert(data.message); // Display success or informational message
            if (data.message.includes("Kod weryfikacyjny")) {
                // Handle verification code flow
                let verificationCode = prompt("Wprowadź kod weryfikacyjny:");
                if (verificationCode) {
                    verifyCode(verificationCode);
                }
            } else {
                window.location.href = "/kalendarz/"; // Redirect to the dashboard or home page
            }
        }
    })
    .catch(error => {
        alert("Wystąpił błąd: " + error);
    });
});

function verifyCode(verificationCode) {
    const data = {
        code: verificationCode
    };

    fetch("/verify-code/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Display error message if any
        } else {
            alert("Kod weryfikacyjny został poprawnie zweryfikowany.");
            window.location.href = "/kalendarz/"; // Redirect to the dashboard or home page
        }
    })
    .catch(error => {
        alert("Wystąpił błąd podczas weryfikacji: " + error);
    });
}
