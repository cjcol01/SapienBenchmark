document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    form.addEventListener("submit", function (e) {
        // Prevent the default form submission
        e.preventDefault();

        // Reset error messages
        document.getElementById("emailError").textContent = "";
        document.getElementById("passwordError").textContent = "";

        // Validate password is not empty
        const password = document.getElementById("password").value;
        if (!password) {
            document.getElementById("passwordError").textContent = "Please enter your password.";
            return;
        }

        // If all checks pass, submit the form
        form.submit();
    });
});
