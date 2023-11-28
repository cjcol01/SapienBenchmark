document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");
    form.addEventListener("submit", function (e) {
        // Prevent the default form submission
        e.preventDefault();

        // Reset error messages
        document.getElementById("emailError").textContent = "";
        document.getElementById("usernameError").textContent = "";
        document.getElementById("passwordError").textContent = "";

        // Validate email (simple validation; update as needed)
        const email = document.getElementById("email").value;
        if (!email.includes("@")) {
            document.getElementById("emailError").textContent = "Please enter a valid email.";
            return;
        }

        // Validate password length and number inclusion
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const passwordRegex = /^(?=.*\d)[A-Za-z\d]{7,}$/; // Regex for minimum 7 characters with at least one number

        if (!passwordRegex.test(password)) {
            document.getElementById("passwordError").textContent =
                "Password must be at least 7 characters long and include at least one number.";
            return;
        }

        // Validate password match
        if (password !== confirmPassword) {
            document.getElementById("passwordError").textContent = "Passwords do not match.";
            return;
        }

        // If all checks pass, submit the form
        form.submit();
    });
});
