document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const button = document.getElementById("loginButton");
    const errorBox = document.getElementById("loginError");
    const toggle = document.getElementById("togglePassword");

    toggle.addEventListener("click", () => {
        const showing = password.type === "text";
        password.type = showing ? "password" : "text";
        toggle.innerHTML = showing
            ? '<i class="bi bi-eye"></i>'
            : '<i class="bi bi-eye-slash"></i>';
        toggle.setAttribute("aria-label", showing ? "Show password" : "Hide password");
    });

    function showError(message) {
        errorBox.textContent = message;
        errorBox.style.display = "block";
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        errorBox.style.display = "none";
        button.disabled = true;
        button.innerHTML = '<i class="bi bi-arrow-repeat spin"></i><span>AUTHENTICATING...</span>';

        try {
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: email.value.trim(),
                    password: password.value
                })
            });

            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.message || "Login failed.");
            }

            window.location.href = data.redirect || "/dashboard";
        } catch (error) {
            showError(error.message || "Unable to connect to the authentication service.");
            button.disabled = false;
            button.innerHTML = '<span>ENTER CONTROL CENTER</span><i class="bi bi-arrow-right"></i>';
        }
    });
});
