document.addEventListener("DOMContentLoaded", () => {

    const loginButton = document.getElementById("login-button");
    const emailField = document.getElementById("txtEmail");
    const passwordField = document.getElementById("txtPassword");

    console.log("Popup script loaded!");
    console.log(loginButton);

    loginButton.addEventListener("click", () => {
        const email = emailField.value;
        const password = passwordField.value;

        console.log("Attempting login...");

        chrome.runtime.sendMessage({command: "login", email, password}, (response) => {
            if (response.result === "success") {
                console.log("Login successful!");
                window.location.href = "home.html";
            } else {
                console.log("Login failed!");
            }
        })
    });
});