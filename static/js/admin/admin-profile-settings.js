

let userId=null;
async function get_me_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`/api/user/me`, null, headers, 'GET');
        
        response.json().then(function(res) {
            
            if (response.status == 200) {
                console.log("This is my res", res);
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

function render_me_data(me_data) {
    document.querySelector("#profileUpdateForm #profile-img-element").src = me_data?.image || '/static/images/admin_profile_image.svg';
    document.querySelector("#profileUpdateForm input[name='name']").value = me_data?.name || '';
    document.querySelector("#profileUpdateForm input[name='email']").value = me_data?.email || '';
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

    // if (!formData.get('phone'))
    //     formData.delete('phone');
    
    try {
        button.disabled = true;
        beforeLoad(button);
        const profileResponse = await updateProfileData(formData);
        if (profileResponse.status === 200) {
            if (imageInput.files.length > 0) {
                
                let adminImageResponse = await updateProfileImage(imageInput.files[0]);
                if (adminImageResponse.status == 200){
                    let adminImageRes = await adminImageResponse.json();
                    document.getElementById("image").src = adminImageRes.data.image;
                }
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
    
    return await requestAPI(`/api/admin/${userId}`, payload, headers, 'PATCH');
}

async function updateProfileImage(imageFile) {
    const imageFormData = new FormData();
    imageFormData.append('image', imageFile);
    const imageHeaders = {
        "X-CSRFToken": getCookie('csrftoken')
    };
    return await requestAPI(`/api/admin/${userId}`, imageFormData, imageHeaders, 'PATCH');
}

function handleProfileUpdateError(errorResponse) {
    let errors = extractErrorMessages(errorResponse);
    showToast("Warning!", errors[0] || "Update failed", "danger-toast");
}

