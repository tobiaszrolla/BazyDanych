// home.js
function showAvailableCourses() {
    const coursesSection = document.getElementById("courses");
    const courseList = document.getElementById("courseList");

    // Przykładowe dane kursów
    const courses = [
        "Kurs kategorii B - Start 15 stycznia",
        "Kurs kategorii B1 - Start 20 stycznia",
        "Kurs kategorii C - Start 25 stycznia"
    ];

    // Dodanie kursów do listy
    courseList.innerHTML = "";
    courses.forEach(course => {
        const li = document.createElement("li");
        li.textContent = course;
        courseList.appendChild(li);
    });

    // Wyświetlenie sekcji kursów
    coursesSection.classList.remove("hidden");
}
