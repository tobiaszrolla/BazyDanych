// info.js
document.addEventListener("DOMContentLoaded", function() {
    // Przykładowe dane kursów
    const courses = [
        {
            name: "Kurs kategorii B",
            startDate: "15 stycznia",
            description: "Kurs przygotowujący do uzyskania prawa jazdy kategorii B."
        },
        {
            name: "Kurs kategorii B1",
            startDate: "20 stycznia",
            description: "Kurs przygotowujący do uzyskania prawa jazdy kategorii B1."
        },
        {
            name: "Kurs kategorii C",
            startDate: "25 stycznia",
            description: "Kurs przygotowujący do uzyskania prawa jazdy kategorii C."
        }
    ];

    const mainSection = document.querySelector("main");

    // Funkcja do wyświetlania kursów
    function displayCourses() {
        const courseSection = document.createElement("section");
        courseSection.innerHTML = `
            <h2>Nasze dostępne kursy</h2>
            <ul id="courseList"></ul>
        `;

        const courseList = courseSection.querySelector("#courseList");

        courses.forEach(course => {
            const li = document.createElement("li");
            li.innerHTML = `
                <strong>${course.name}</strong> - Start: ${course.startDate}<br>
                <em>${course.description}</em>
            `;
            courseList.appendChild(li);
        });

        mainSection.appendChild(courseSection);
    }

    // Wywołanie funkcji displayCourses
    displayCourses();
});
