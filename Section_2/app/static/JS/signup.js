document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");
    form.addEventListener("submit", function (e) {
        // Prevent the default form submission
        e.preventDefault();

        // Reset error messages
        document.getElementById("emailError").textContent = "";
        document.getElementById("usernameError").textContent = "";
        document.getElementById("passwordError").textContent = "";

        // Validate password length and number inclusion
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const passwordRegex = /^(?=.*\d)[A-Za-z\d]{7,}$/; // Regex pfor minimum 7 characters with at least one number

        // Validate password match
        if (password !== confirmPassword) {
            document.getElementById("passwordError").textContent = "Passwords do not match.";
            return;
        }
        // Validate password is complex 
        if (!passwordRegex.test(password)) {
            document.getElementById("passwordError").textContent =
                "Password must be at least 7 characters long and include at least one number.";
            return;
        }

        // AJAX request to check if email is already registered
        $.post("/check_email", { email: email }, function (data) {
            if (data.isTaken) {
                console.log("Email already registered");
                document.getElementById("passwordError").textContent =
                    "Email is already registered.";
            } else {
                // If all checks pass, submit the form
                form.submit();
            }
        });

        // // If all checks pass, submit the form
        // form.submit();
    });
});
