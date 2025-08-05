

let form = document.querySelector("#loginForm");
form.addEventListener("submit", loginForm)

async function loginForm(event) {
    event.preventDefault();
    const form = event.target;
    const button = form.querySelector(`button[type="submit"]`);
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl.textContent;
    const formData = new FormData(form);
    const data = formDataToObject(formData);

    if (!data.email || !data.password) {
        showToast("Warning!", "Both email and password are required", "danger-toast");
        return;
    }

    if (!emailRegex.test(data.email)) {
        showToast("Warning!", "Please enter a valid email address", "danger-toast");
        return;
    }

    try {
        let headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        button.disabled = true;
        beforeLoad(button);
        const response = await requestAPI(`${API_BASE_URL}login`, JSON.stringify(data), headers, 'POST');
        
        if (response.status == 200) {
            showToast("Success", "Logged in successfully!", "success-toast");
            setTimeout(() => {
                afterLoad(button, "Signed in");
                location.href = `/keep-it-clean/`;
            }, 1000);
        } else {
            const result = await response.json();
            afterLoad(button, originalButtonText);
            let errors = extractErrorMessages(result);
            showToast("Warning!", errors[0] || "Login failed.", "danger-toast");
            button.disabled = false;
        }
    } catch (error) {
        console.error("Login error:", error);
        let errors = extractErrorMessages(result);
        showToast("Error!", errors[0], "danger-toast");
        button.disabled = false;
        afterLoad(button, originalButtonText);
    }
}

