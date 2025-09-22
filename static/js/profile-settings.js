let userId=null;
async function get_me_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}user/me`, null, headers, 'GET');
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
    
    if (!validateProfileForm(formData)) return;
    formData.delete("image")

    if (!formData.get('phone'))
        formData.delete('phone');
    
    try {
        button.disabled = true;
        beforeLoad(button);
        const profileResponse = await updateProfileData(formData);
        if (profileResponse.status === 200) {
            if (imageInput.files.length > 0) {
                await updateProfileImage(imageInput.files[0]);
            }
            showToast("Success", "Profile updated successfully!", "success-toast");
            setTimeout(() => {
                afterLoad(button, "Updated");
                buttonTextEl.textContent = originalButtonText;
                _get_me_data();
                get_me_data();
            }, 1000);
        } else {
            handleProfileUpdateError(await profileResponse.json());
        }
    } catch (error) {
        console.error("Update error:", error);
        showToast("Error!", "Failed to update profile", "danger-toast");
    } finally {
        button.disabled = false;
        afterLoad(button, originalButtonText);
    }
}

function validateProfileForm(formData) {
    if (!formData.get('name')) {
        showToast("Warning!", "Name is required", "danger-toast");
        return false;
    }
    
    if (!formData.get('email')) {
        showToast("Warning!", "Email is required", "danger-toast");
        return false;
    }
    
    if (!emailRegex.test(formData.get('email'))) {
        showToast("Warning!", "Please enter a valid email address", "danger-toast");
        return false;
    }
    
    return true;
}

async function updateProfileData(formData) {
    const data = {};
    formData.forEach((value, key) => data[key] = value);
    
    const payload = JSON.stringify(data);
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    };
    
    return await requestAPI(`${API_BASE_URL}user/${userId}`, payload, headers, 'PATCH');
}

async function updateProfileImage(imageFile) {
    const imageFormData = new FormData();
    imageFormData.append('image', imageFile);
    const imageHeaders = {
        "X-CSRFToken": getCookie('csrftoken')
    };
    return await requestAPI(`${API_BASE_URL}user/${userId}`, imageFormData, imageHeaders, 'PATCH');
}

function handleProfileUpdateError(errorResponse) {
    let errors = extractErrorMessages(errorResponse);
    showToast("Warning!", errors[0] || "Update failed", "danger-toast");
}

function openUpdatePasswordModal() {
    let modalId = "updatePassword";
    let modal = document.querySelector(`#${modalId}`);
    let form = modal.querySelector("form");
    modal.addEventListener('hidden.bs.modal', event => {
        form.reset();
    })
    document.querySelector(`.${modalId}`).click();
}

let passwordChangeForm = document.querySelector('#UpdatePasswordForm');
passwordChangeForm.addEventListener('submit', async (event) => {
    event.preventDefault(); 
    const formData = new FormData(passwordChangeForm);
    const data = Object.fromEntries(formData);
    let button = document.querySelector("button[form='UpdatePasswordForm']");
    let buttonText = button.querySelector(".btn-text").textContent;

    if (!data.old_password) {
        showToast("Warning!", "Current password is required", "danger-toast");
        return false;
    }

    if (!data.new_password || data.new_password.length < 8) {
        showToast("Warning!", "New password must be at least 8 characters", "danger-toast");
        return false;
    }

    if (data.new_password !== data.confirm_password) {
        showToast("Warning!", "Passwords do not match", "danger-toast");
        return false;
    }

    if (data.new_password === data.old_password) {
        showToast("Warning!", "New password cannot be the same as current password", "danger-toast");
        return false;
    }

    try {
        let headers = {
            "X-CSRFToken": getCookie('csrftoken'),
            "Content-Type": "application/json" 
        };
        beforeLoad(button);
        const jsonData = JSON.stringify({
            old_password: data.old_password,
            new_password: data.new_password,
            confirm_password: data.confirm_password
        });
        let response = await requestAPI(`/api/user/password/update`, jsonData, headers, 'PATCH');
        if (response.status == 200) {
            showToast("Success", "Password updated successfully!", "success-toast");
            afterLoad(button, 'Updated');
            button.disabled = true;
            setTimeout(() => {
                button.disabled = false;
                afterLoad(button, buttonText);
                closeCurrentModal();
                passwordChangeForm.reset();
            }, 1500);
        } else {
            afterLoad(button, buttonText);
            const result = await response.json();
            let errors = extractErrorMessages(result);
            showToast("Warning!", errors[0] || "Password update failed", "danger-toast");
        }
    } catch (err) {
        afterLoad(button, buttonText);
        showToast("Error!", "An error occurred while updating password", "danger-toast");
        console.error("Password update error:", err);
    }
});