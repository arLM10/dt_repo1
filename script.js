// script.js

// 1. Change theme on button click
function toggleTheme() {
    let body = document.body;
    
    // Check if the current background is light (white or default)
    if (body.style.backgroundColor === "white" || body.style.backgroundColor === "" || body.style.backgroundColor === "rgb(245, 245, 245)") {
        // Apply Dark Mode
        body.style.backgroundColor = "#2c3e50"; // Dark Blue/Grey
        body.style.color = "white";
        // Also adjust the list and form backgrounds for contrast
        document.querySelectorAll('ul, #contact-form').forEach(element => {
            element.style.backgroundColor = "#34495e";
        });
        document.querySelectorAll('h1, h2').forEach(element => {
            element.style.color = "#3498db"; // Lighter heading color
        });
    } else {
        // Apply Light Mode (Revert to default/CSS values)
        body.style.backgroundColor = ""; // Revert to CSS default (#f5f5f5)
        body.style.color = ""; // Revert to CSS default (#333)
        
        document.querySelectorAll('ul').forEach(element => {
            element.style.backgroundColor = "white";
        });
        document.getElementById('contact-form').style.backgroundColor = "#ecf0f1";
        
        document.querySelector('h1').style.color = "#2c3e50";
        document.querySelectorAll('h2').forEach(element => {
            element.style.color = "#34495e";
        });
    }
}


// 2. Add a click counter
let counter = 0;
function countClicks() {
    counter++;
    document.getElementById("clickCount").textContent = "Clicks: " + counter;
}

// 3. Form validation and Submission Handling
document.addEventListener('DOMContentLoaded', () => {
    let form = document.getElementById("messageForm");

    // Check if the form element exists before adding the listener
    if (form) {
        form.addEventListener("submit", function (event) {
            // Prevent the default form submission (page reload)
            event.preventDefault(); 
            
            // Get values from the input fields
            let nameInput = document.getElementById('name');
            let emailInput = document.getElementById('email');
            let messageInput = document.getElementById('message');
            
            let name = nameInput.value.trim();
            let email = emailInput.value.trim();

            // Simple validation
            if (name === "" || email === "") {
                alert("Please fill in both your Name and Email fields!");
            } else {
                // Success message
                alert(`Thank you, ${name}! Your message has been sent successfully.`);
                
                // Clear the form fields
                form.reset();
            }
        });
    }
});
