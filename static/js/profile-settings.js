let userId=null;
async function get_me_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}me`, null, headers, 'GET');
        response.json().then(function(res) {
            if (response.status == 200) {
                render_me_data(res);
                userId = res.id;
            }
            else {
                console.log(res)
                return false;
            }
        })
    }
    catch (err) {
        console.log(err);
    }
}

window.addEventListener('load', get_me_data());

function render_me_data(me_data){
    document.querySelector("#profileUpdateForm img").src = me_data?.image || '/static/images/admin_profile_image.svg';
    document.querySelector("#profileUpdateForm input[name='name']").value = me_data?.name || '';
    document.querySelector("#profileUpdateForm input[name='email']").value = me_data?.email || '';
    document.querySelector("#profileUpdateForm input[name='phone']").value = me_data?.phone || '';
}

let form = document.querySelector("#profileUpdateForm");
form.addEventListener("submit", profileUpdateForm)

async function profileUpdateForm(event) {
    event.preventDefault();
    const form = event.target;
    const button = form.querySelector('button[type="submit"]');
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl.textContent;
    const formData = new FormData(form);
    const imageInput = form.querySelector('input[type="file"]');
    
    if (!formData.get('name')) {
        showToast("Warning!", "Name is required", "danger-toast");
        return;
    }
    if (!formData.get('email')) {
        showToast("Warning!", "Email is required", "danger-toast");
        return;
    }
    if (!emailRegex.test(formData.get('email'))) {
        showToast("Warning!", "Please enter a valid email address", "danger-toast");
        return;
    }

    try {
        button.disabled = true;
        beforeLoad(button);
        
        let payload;
        let headers;
        
        if (imageInput.files.length > 0) {
            headers = {
                'X-CSRFToken': getCookie('csrftoken')
            };
            payload = formData;
        } else {
            headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            };
            const data = {};
            formData.forEach((value, key) => data[key] = value);
            payload = JSON.stringify(data);
        }

        const response = await requestAPI(`${API_BASE_URL}user/${userId}`,payload, headers, 'PATCH');

        if (response.status == 200) {
            showToast("Success", "Profile updated successfully!", "success-toast");
            setTimeout(() => {
                afterLoad(button, "Updated");
                buttonTextEl.textContent = originalButtonText;
                _get_me_data();
                get_me_data();
            }, 1000);
        } else {
            const result = await response.json();
            let errors = extractErrorMessages(result);
            showToast("Warning!", errors[0] || "Update failed", "danger-toast");
        }
    } catch (error) {
        console.error("Update error:", error);
        showToast("Error!", "Failed to update profile", "danger-toast");
    } finally {
        button.disabled = false;
        afterLoad(button, originalButtonText);
    }
}
