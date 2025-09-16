let phoneNumberInput = document.getElementById("phone");

async function contactFormSubmit(event) {
    event.preventDefault();

    let form = event.target;
    let button = document.querySelector('#contact_button');
    let buttonText = button.querySelector(".btn-text").textContent;
    let formData = new FormData(form);
    let data = formDataToObject(formData);

    const phoneNumber = libphonenumber.isValidPhoneNumber(data.phone_number);

    // 📌 Phone validation
    if (!phoneNumber) {
        showToast("Error!", "Please enter a valid phone number with country code.", "danger-toast");
        return false;
    }

    // 📌 Validations
    if (!data.first_name || data.first_name.trim() === '') {
        showToast("Error!", "First name is required.", "danger-toast");
        return false;
    }
    if (!data.last_name || data.last_name.trim() === '') {
        showToast("Error!", "Last name is required.", "danger-toast");
        return false;
    }
    if (!data.email || data.email.trim() === '') {
        showToast("Error!", "Email is required.", "danger-toast");
        return false;
    }
    if (!data.service_type || data.service_type.trim() === '') {
        showToast("Error!", "Please select a service type.", "danger-toast");
        return false;
    }
    if (!data.message || data.message.trim() === '') {
        showToast("Error!", "Message is required.", "danger-toast");
        return false;
    }

    // 📌 Payload
    let payload = {
        first_name: data.first_name.trim(),
        last_name: data.last_name.trim(),
        email: data.email.trim(),
        phone_number: data.phone_number,
        service_type: "healthy_home_evaluation",
        message: data.message?.trim() || '',
    };

    // 📌 Headers
    let headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrfmiddlewaretoken,
    };

    try {
        beforeLoad(button);

        let response = await requestAPI('/api/contact-us/', JSON.stringify(payload), headers, 'POST');

        response.json().then(function (res) {
            if (response.ok) {
                showToast("Success!", "Your message has been sent successfully.", "success-toast");
                form.reset();
                button.disabled = true;
                afterLoad(button, 'Sent');
                let successModal = new bootstrap.Modal(document.getElementById('successModal'));
                successModal.show();
                setTimeout(() => {
                    afterLoad(button, buttonText);
                    button.disabled = false;
                }, 2000);
            } else {
                afterLoad(button, buttonText);
                if (typeof res === "object") {
                    Object.values(res).forEach(err => {
                        showToast("Error!", err, "danger-toast");
                    });
                } else {
                    showToast("Error!", "Something went wrong. Please try again.", "danger-toast");
                }
            }
        });

    } catch (err) {
        console.error(err);
        afterLoad(button, buttonText);
        showToast("Error!", "Something went wrong. Please try again.", "danger-toast");
    }
}

document.querySelector("#contact_form").addEventListener("submit", contactFormSubmit);



function handlePhoneInput(e) {
    const input = e.target;
    let value = input.value;
    
    // Remove all characters except digits and +
    value = value.replace(/[^\d+]/g, '');
    
    // Ensure + can only be at the beginning
    if (value.includes('+')) {
        const plusIndex = value.indexOf('+');
        if (plusIndex === 0) {
            value = '+' + value.substring(1).replace(/\+/g, '');
        } else {
            value = value.replace(/\+/g, '');
        }
    }
    
    input.value = value;
};


function handlePhoneKeyPress(e) {
    const char = e.key;
    const currentValue = e.target.value;
    const cursorPosition = e.target.selectionStart;
    
    // Allow backspace, delete, arrow keys, tab, etc.
    if (e.key.length > 1) return;
    
    if (char === '+' && cursorPosition === 0 && !currentValue.includes('+')) {
        return;
    }
    
    if (/\d/.test(char)) {
        return;
    }
    
    // Block all other characters
    e.preventDefault();
};

phoneNumberInput.addEventListener('input', handlePhoneInput);
phoneNumberInput.addEventListener('keypress', handlePhoneKeyPress);