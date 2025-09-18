

let form = document.querySelector("#registerForm");
form.addEventListener("submit", registerForm)

async function registerForm(event) {
    event.preventDefault();
    const form = event.target;
    const button = form.querySelector(`button[type="submit"]`);
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl.textContent;
    const formData = new FormData(form);
    const data = formDataToObject(formData);

    // Password validation checks
    const containsUppercase = /[A-Z]/.test(data.password);
    const containsLowercase = /[a-z]/.test(data.password);
    const containsDigit = /\d/.test(data.password);
    let passwordRegex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/; 
    const containsSpecialChar = passwordRegex.test(data.password);

    if (!data.name) {
        showToast("Warning!", "Name is required", "danger-toast");
        return;
    }

    if (!data.email) {
        showToast("Warning!", "Email is required", "danger-toast");
        return;
    }

    if (!emailRegex.test(data.email)) {
        showToast("Warning!", "Please enter a valid email address", "danger-toast");
        return;
    }

    if (data.password.length < 8) {
        showToast("Warning!", "Password must be at least 8 characters long", "danger-toast");
        return false;
    }
    else if (data.password !== data.confirm_password) {
        showToast("Warning!", "Password and Confirm Password must match", "danger-toast");
        return false;
    }
    else if (!containsUppercase) {
        showToast("Warning!", "Password must contain at least one uppercase letter", "danger-toast");
        return false;
    }
    else if (!containsLowercase) {
        showToast("Warning!", "Password must contain at least one lowercase letter", "danger-toast");
        return false;
    }
    else if (!containsDigit) {
        showToast("Warning!", "Password must contain at least one digit", "danger-toast");
        return false;
    }
    else if (!containsSpecialChar) {
        showToast("Warning!", "Password must contain at least one special character", "danger-toast");
        return false;
    }

    try {
        let headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        button.disabled = true;
        beforeLoad(button);
        const response = await requestAPI(`${API_BASE_URL}user`, JSON.stringify(data), headers, 'POST');
        
        if (response.status == 201) {
            showToast("Success", "User has been created successfully. Please log in to proceed.", "success-toast");
            setTimeout(() => {
                afterLoad(button, "Signed in");
                location.href = `/login-page/`;
            }, 1000);
        } else {
            const result = await response.json();
            afterLoad(button, originalButtonText);
            let errors = extractErrorMessages(result);
            showToast("Warning!", errors[0] || "Registration failed.", "danger-toast");
            button.disabled = false;
        }
    } catch (error) {
        console.error("Registration error:", error);
        let errors = extractErrorMessages(result);
        showToast("Error!", errors[0], "danger-toast");
        button.disabled = false;
        afterLoad(button, originalButtonText);
    }
}

