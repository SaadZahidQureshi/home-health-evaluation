const API_BASE_URL = JSON.parse(document.getElementById("API_BASE_URL").textContent);
const emailRegex = /^[a-z0-9](?:[a-z0-9._%+-]*[a-z0-9])?@[a-z0-9.-]+\.[a-z]{2,}$/i;
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
    
    // Use the container as the node option
    Toastify({
        // node: toastContent,
        text: body,
        duration: 5000, // 5 seconds
        close: true,
        gravity: "top", // top or bottom
        position: "right", // left, center or right
        className: className,
        stopOnFocus: true, // Prevents dismissing of toast on hover
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
    // let maxTries = tries;
    const response = await fetch(url, {
        method: method,
        mode: 'cors',
        headers: headers,
        body: data,
    });
    // maxTries++;
    // if (response.status == 401) {
    //     if(maxTries > 3) return response;
    //     console.log(maxTries);
    //     let refreshResponse = await onRefreshToken(maxTries);
    //     if (refreshResponse.status == 200) {
    //         let refreshRes = await refreshResponse.json();
    //         const accessToken = parseJwt(refreshRes.access);
    //         setCookie("user_access", refreshRes.access, accessToken.exp);
    //         headers['Authorization'] = `Bearer ${refreshRes.access}`;
    //         return await requestAPI(url, data, headers, method, maxTries);
    //     }
    //     else {
    //         clearUserTokens();
    //         const currentPath = window.location.pathname;
    //         const isAuthPage = authPages.some(page => currentPath.includes(page));
    //         if (isAuthPage) return;

    //         location.href = location.origin + '/administration/login/';
    //         return;
    //     }
    // }
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
