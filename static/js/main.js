const API_BASE_URL = JSON.parse(document.getElementById("API_BASE_URL").textContent);
const emailRegex = /^[a-z0-9](?:[a-z0-9._%+-]*[a-z0-9])?@[a-z0-9.-]+\.[a-z]{2,}$/i;
let logout_form = document.querySelector("#logoutForm");
logout_form?.addEventListener("submit", logoutForm)
let principle_status_data = null;
window.addEventListener('load', () =>{_get_me_data(); _get_principle_data()});

(function ($) {

    $(document).ready(function () {

        // Hamburger-menu
        $('.hamburger-menu').on('click', function () {
            $('.hamburger-menu .line-top, .main-left-col, .right-mainpart').toggleClass('current');
            $('.hamburger-menu .line-center').toggleClass('current');
            $('.hamburger-menu .line-bottom').toggleClass('current');
        });


        // accordian ----------
        $(".accordian_cnt").click(function() {
            $(this).toggleClass("active").next().slideToggle();
        });

    });

})(jQuery);

function formDataToObject(formData){
    let object = {}
    formData.forEach((key, value) => {
        object[value] = key; 
    })
    return object;
}

function showToast(title, body, className) {
    Toastify({
        text: body,
        duration: 5000,
        close: true,
        gravity: "top",
        position: "right",
        className: className,
        stopOnFocus: true,
    }).showToast();
}

function beforeLoad(button) {
    button.querySelector('.btn-text').innerText = '';
    button.querySelector('.spinner-border').classList.remove('hide');
    button.disabled = true;
    button.style.cursor ='not-allowed';
    button.pointerEvents = "none";
}

function afterLoad(button, text) {
    button.querySelector('.btn-text').innerText = text;
    button.querySelector('span').classList.add('hide');
    button.disabled = false;
    button.style.cursor ='pointer';
    button.pointerEvents = "auto";
}

function extractErrorMessages(obj) {
	const messages = [];

	function retrieve(currentObj) {
		for (const key in currentObj) {
			if (Object.hasOwnProperty.call(currentObj, key)) {
				const value = currentObj[key];

				if (Array.isArray(value)) {
					value.forEach(item => {
						if (typeof item === 'object' && item !== null) {
							retrieve(item);
						} else {
							messages.push(item);
						}
					});
				} else if (typeof value === 'object' && value !== null) {
					retrieve(value);
				} else {
					messages.push(value);
				}
			}
		}
	}

	retrieve(obj);
	return messages;
}

function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const toggleBtn = passwordField.nextElementSibling;
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3.3" stroke="#98FB98" stroke-width="1.4"/>
                <path d="M20.188 10.9343C20.5762 11.4056 20.7703 11.6412 20.7703 12C20.7703 12.3588 20.5762 12.5944 20.188 13.0657C18.7679 14.7899 15.6357 18 12 18C8.36427 18 5.23206 14.7899 3.81197 13.0657C3.42381 12.5944 3.22973 12.3588 3.22973 12C3.22973 11.6412 3.42381 11.4056 3.81197 10.9343C5.23206 9.21014 8.36427 6 12 6C15.6357 6 18.7679 9.21014 20.188 10.9343Z" stroke="#98FB98" stroke-width="1.7"/>
            </svg>
        `;
    } else {
        passwordField.type = 'password';
        toggleBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3.3" stroke="#98FB98" stroke-width="1.4"></circle>
                <path d="M20.188 10.9343C20.5762 11.4056 20.7703 11.6412 20.7703 12C20.7703 12.3588 20.5762 12.5944 20.188 13.0657C18.7679 14.7899 15.6357 18 12 18C8.36427 18 5.23206 14.7899 3.81197 13.0657C3.42381 12.5944 3.22973 12.3588 3.22973 12C3.22973 11.6412 3.42381 11.4056 3.81197 10.9343C5.23206 9.21014 8.36427 6 12 6C15.6357 6 18.7679 9.21014 20.188 10.9343Z" stroke="#98FB98" stroke-width="1.7"></path>
                <path d="M20 5L5 20" stroke="#98FB98" stroke-width="1.5" stroke-linecap="round"></path>
            </svg>
        `;
    }
}

async function requestAPI(url, data, headers, method, tries=0) {
    const response = await fetch(url, {
        method: method,
        mode: 'cors',
        headers: headers,
        body: data,
    });
    return response; 
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function _get_me_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}me`, null, headers, 'GET');
        response.json().then(function(res) {
            if (response.status == 200) {
                _render_me_data(res);
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

function _render_me_data(me_data){
    document.querySelector("#image").src = me_data?.image || '/static/images/admin_profile_image.svg';
}

function UploadImage(event){
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector(".avatar-icon").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

async function handleLogout() {
    const modalId = "logoutModal";
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    const form = document.getElementById("logoutForm");
    modal._element.addEventListener('hidden.bs.modal', function() {
        form.reset();
    });
    modal.show();
}

async function logoutForm(event) {
    event.preventDefault();
    const form = event.target;
    const button = document.querySelector(`button[form="${form.id}"]`);
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl.textContent;

    try {
        let headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        };
        button.disabled = true;
        beforeLoad(button);
        const response = await requestAPI(`${API_BASE_URL}logout`, null, headers, 'POST');
        
        if (response.status == 200) {
            showToast("Success", "Logged out successfully!", "success-toast");
            setTimeout(() => {
                afterLoad(button, "Signed in");
                sessionStorage.removeItem("customer_id")
                location.href = `/`;
            }, 1000);
        } else {
            const result = await response.json();
            afterLoad(button, originalButtonText);
            let errors = extractErrorMessages(result);
            showToast("Warning!", errors[0] || "Logging out failed.", "danger-toast");
            button.disabled = false;
        }
    } catch (error) {
        console.error("Logout error:", error);
        let errors = extractErrorMessages(result);
        showToast("Error!", errors[0], "danger-toast");
        button.disabled = false;
        afterLoad(button, originalButtonText);
    }
}

async function get_principle_status_data() {
    let customer_id = sessionStorage.getItem("customer_id") || null;
    try {
        let headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        };

        let endpoint = `${API_BASE_URL}principles/status`;
        if (customer_id) {endpoint += `?customer_id=${customer_id}`;}
        let response = await requestAPI(endpoint, null, headers, "GET");
        let res = await response.json();

        if (response.status === 200) {
            principle_status_data = res;
            render_principle_status_data(principle_status_data);
        } else {
            console.log(res);
            return false;
        }
    } catch (err) {
        console.error(err);
    }
}

function render_principle_status_data(data) {
    let container = document.querySelector(".side_menu > ul");
    data.forEach(item => {
        let el = container.querySelector(`#principle-${item.id}`);
        if (el) {
            el.classList.add(item?.status || "");
        }
    });
}

async function _get_principle_data() {
    try {
        let headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        };
        let endpoint = `${API_BASE_URL}principles`;
        let response = await requestAPI(endpoint, null, headers, "GET");
        let res = await response.json();
        if (response.status === 200) {
            _attachItemListeners(res.data);
        } else {
            console.log(res);
            return false;
        }
    } catch (err) {
        console.error(err);
    }
}

function _attachItemListeners(data) {
    let items = document.querySelectorAll(".side_menu > ul > li");

    items.forEach((item, index) => {
        if (data[index]) {
            item.id = `principle-${data[index].id}`;
        }
    });

    get_principle_status_data();
}

async function successModal(){
    let modalId = "successmodal";
    let modal_el = document.getElementById(modalId)
    const modal = new bootstrap.Modal(modal_el);
    const form = modal_el.querySelector("form");
    modal._element.addEventListener('hidden.bs.modal', function() {
        form.reset();
        sessionStorage.removeItem("customer_id");
        location.href = "/keep-it-clean/";
    });
    modal.show();
}

function uploadIdImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgElement = document.querySelector('#id_image_preview');
            imgElement.src = e.target.result;
            imgElement.classList.remove("hide");
        };
        reader.readAsDataURL(file);
        hasUploadedIdImage = true;
    }
}

function addNewCustomerRecord(event){
    event.preventDefault();
    sessionStorage.removeItem("customer_id");
    location.href = "/keep-it-clean/";
}

function formatDate(inputDate) {
    const date = new Date(inputDate);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
}
