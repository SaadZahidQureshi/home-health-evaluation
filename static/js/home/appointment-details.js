var successModal;
let nextActionsModal;
let appointmentData = {};
let isEditMode = false;

// Initialize modals when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    successModal = new bootstrap.Modal(document.getElementById('successModal'));
    nextActionsModal = new bootstrap.Modal(document.getElementById('nextActionsModal'));
});

// Open success modal
function openSuccessModal() {
    successModal.show();
}

// Continue to next button action
function continueToNext() {
    successModal.hide();
    // Add your custom logic here
}

// Save to calendar button action
function saveToCalendar() {
    successModal.hide();
    setTimeout(() => {
        nextActionsModal.show();
    }, 300);
}

// Go back from second modal
function goBack() {
    nextActionsModal.hide();
    setTimeout(() => {
        successModal.show();
    }, 300);
}

function scheduleNew() {
    console.log('Schedule New Appointment clicked');
    nextActionsModal.hide();
    location.pathname = '/book-appointments/';
    // Add your custom logic here
}



async function appointmentFormSubmit(event) {
    event.preventDefault();

    let form = event.target;
    let button = form.querySelector(".book-button");
    let buttonText = button.querySelector('.btn-text').innerText;

    let formData = new FormData(form);
    let data = Object.fromEntries(formData.entries());

    // 📌 SessionStorage data
    let selectedDate = sessionStorage.getItem("selected_date");
    let selectedSlot = sessionStorage.getItem("selected_slot");

    // -------- Validations --------
    if (!isEditMode) { 
        if (!selectedDate || !selectedSlot) {
            showToast("Error!", "Please select a date and slot before booking.", "danger-toast");
            return false;
        }
    }
    if (!data.first_name || data.first_name.trim() === "") {
        showToast("Error!", "First name is required.", "danger-toast");
        return false;
    }
    if (!data.last_name || data.last_name.trim() === "") {
        showToast("Error!", "Last name is required.", "danger-toast");
        return false;
    }
    if (!data.email || data.email.trim() === "") {
        showToast("Error!", "Email is required.", "danger-toast");
        return false;
    }
    if (!data.phone_number || data.phone_number.trim() === "") {
        showToast("Error!", "Phone number is required.", "danger-toast");
        return false;
    }
    if (!data.address || data.address.trim() === "") {
        showToast("Error!", "Address is required.", "danger-toast");
        return false;
    }
    if (!data.zip_code || data.zip_code.trim() === "") {
        showToast("Error!", "Zip code is required.", "danger-toast");
        return false;
    }
    if (!data.city || data.city.trim() === "") {
        showToast("Error!", "City is required.", "danger-toast");
        return false;
    }
    if (!data.state || data.state.trim() === "") {
        showToast("Error!", "State is required.", "danger-toast");
        return false;
    }

    // -------- Payload --------
    let payload = {
        first_name: data.first_name.trim(),
        last_name: data.last_name.trim(),
        email: data.email.trim(),
        phone_number: data.phone_number.trim(),
        address: data.address.trim(),
        zip_code: data.zip_code.trim(),
        city: data.city.trim(),
        state: data.state.trim(),
        notes: data.notes?.trim() || ""
    };

    if (!isEditMode) {
        payload.date = selectedDate;
        payload.slot_type = selectedSlot;
    }

    let headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrfmiddlewaretoken
    };

    try {
        beforeLoad(button);

        let response, res;

        if (isEditMode) {
            // 📌 Update booking person
            let bookingPersonId = appointmentData.booking_person?.id;
            response = await fetch(`${API_BASE_URL}booking-person/${bookingPersonId}`, {
                method: "PUT",
                headers: headers,
                body: JSON.stringify(payload)
            });
            res = await response.json();
        } else {
            // 📌 Create new appointment
            response = await fetch(`${API_BASE_URL}appointments`, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(payload)
            });
            res = await response.json();
        }

        if (response.ok) {
            if (isEditMode) {
                appointmentData.booking_person = res;
                showToast("Success!", "Your appointment details have been updated.", "success-toast");
                isEditMode = false;
            } else {
                appointmentData = res;
                sessionStorage.setItem("appointment_id", res.id);
                sessionStorage.removeItem("selected_date");
                sessionStorage.removeItem("selected_slot");
                showToast("Success!", "Your appointment has been booked successfully.", "success-toast");
            }

            renderAppointmentDataInModal();
            openSuccessModal();

            afterLoad(button, isEditMode ? "Updated" : "Booked");
            button.disabled = true;

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

    } catch (err) {
        console.error(err);
        afterLoad(button, buttonText);
        showToast("Error!", "Something went wrong. Please try again.", "danger-toast");
    }
}

// 📌 Attach listener
document.querySelector(".booking-form").addEventListener("submit", appointmentFormSubmit);


function renderAppointmentDataInModal() {
    let container = document.getElementById("AppointmentData");
    container.innerHTML = `
        <div class="info-item">
                            <div class="info-icon">
                                <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="34" height="34" rx="17" fill="white"/>
                                    <path d="M16.9997 15C17.7954 15 18.5584 14.6839 19.121 14.1213C19.6836 13.5587 19.9997 12.7956 19.9997 12C19.9997 11.2044 19.6836 10.4413 19.121 9.87868C18.5584 9.31607 17.7954 9 16.9997 9C16.2041 9 15.441 9.31607 14.8784 9.87868C14.3158 10.4413 13.9997 11.2044 13.9997 12C13.9997 12.7956 14.3158 13.5587 14.8784 14.1213C15.441 14.6839 16.2041 15 16.9997 15ZM10.4647 21.493C10.3719 21.7411 10.3616 22.0126 10.4355 22.267C10.5094 22.5214 10.6634 22.7452 10.8747 22.905C12.626 24.266 14.7817 25.0034 16.9997 25C19.3097 25 21.4377 24.216 23.1307 22.9C23.5607 22.567 23.7347 21.997 23.5387 21.49C23.0309 20.168 22.1343 19.0311 20.967 18.2292C19.7998 17.4274 18.4168 16.9983 17.0007 16.9986C15.5845 16.9989 14.2018 17.4287 13.0349 18.231C11.868 19.0334 10.9719 20.1708 10.4647 21.493Z" fill="url(#paint0_linear_1154_615)"/>
                                    <defs>
                                    <linearGradient id="paint0_linear_1154_615" x1="17.0028" y1="9" x2="17.0028" y2="25" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#71BF1E"/>
                                    <stop offset="1" stop-color="#71BF1E"/>
                                    </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <div class="info-text">
                                <strong>${appointmentData.booking_person.first_name} ${appointmentData.booking_person.last_name}</strong><br>
                                ${appointmentData.booking_person.email}
                            </div>
                        </div>
                        <div class="info-item">
                            <div class="info-icon">
                                <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="34" height="34" rx="17" fill="white"/>
                                    <path fill-rule="evenodd" clip-rule="evenodd" d="M16.69 25.933L16.693 25.934C16.89 26.02 17 26 17 26C17 26 17.11 26.02 17.308 25.934L17.31 25.933L17.316 25.93L17.334 25.922C17.4289 25.8779 17.5226 25.8312 17.615 25.782C17.801 25.686 18.061 25.542 18.372 25.349C18.992 24.965 19.817 24.383 20.646 23.584C22.302 21.988 24 19.493 24 16C24 15.0807 23.8189 14.1705 23.4672 13.3212C23.1154 12.4719 22.5998 11.7003 21.9497 11.0503C21.2997 10.4002 20.5281 9.88463 19.6788 9.53284C18.8295 9.18106 17.9193 9 17 9C16.0807 9 15.1705 9.18106 14.3212 9.53284C13.4719 9.88463 12.7003 10.4002 12.0503 11.0503C11.4002 11.7003 10.8846 12.4719 10.5328 13.3212C10.1811 14.1705 10 15.0807 10 16C10 19.492 11.698 21.988 13.355 23.584C14.0488 24.2503 14.8106 24.8419 15.628 25.349C15.9446 25.5456 16.2703 25.7271 16.604 25.893L16.666 25.922L16.684 25.93L16.69 25.933ZM17 18.25C17.5967 18.25 18.169 18.0129 18.591 17.591C19.0129 17.169 19.25 16.5967 19.25 16C19.25 15.4033 19.0129 14.831 18.591 14.409C18.169 13.9871 17.5967 13.75 17 13.75C16.4033 13.75 15.831 13.9871 15.409 14.409C14.9871 14.831 14.75 15.4033 14.75 16C14.75 16.5967 14.9871 17.169 15.409 17.591C15.831 18.0129 16.4033 18.25 17 18.25Z" fill="url(#paint0_linear_1154_650)"/>
                                    <defs>
                                    <linearGradient id="paint0_linear_1154_650" x1="17" y1="9" x2="17" y2="26.002" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#71BF1E"/>
                                    <stop offset="1" stop-color="#71BF1E"/>
                                    </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <div class="info-text">${appointmentData.booking_person.address}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-icon">
                               <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="34" height="34" rx="17" fill="white"/>
                                    <path fill-rule="evenodd" clip-rule="evenodd" d="M11.5 9C11.1022 9 10.7206 9.15804 10.4393 9.43934C10.158 9.72065 10 10.1022 10 10.5V23.5C10 23.8978 10.158 24.2794 10.4393 24.5607C10.7206 24.842 11.1022 25 11.5 25H22.5C22.8978 25 23.2794 24.842 23.5607 24.5607C23.842 24.2794 24 23.8978 24 23.5V14.621C23.9997 14.2233 23.8414 13.842 23.56 13.561L19.44 9.439C19.3005 9.29961 19.1349 9.1891 18.9527 9.11377C18.7705 9.03844 18.5752 8.99978 18.378 9H11.5ZM13.75 17.5C13.5511 17.5 13.3603 17.579 13.2197 17.7197C13.079 17.8603 13 18.0511 13 18.25C13 18.4489 13.079 18.6397 13.2197 18.7803C13.3603 18.921 13.5511 19 13.75 19H20.25C20.4489 19 20.6397 18.921 20.7803 18.7803C20.921 18.6397 21 18.4489 21 18.25C21 18.0511 20.921 17.8603 20.7803 17.7197C20.6397 17.579 20.4489 17.5 20.25 17.5H13.75ZM13.75 20.5C13.5511 20.5 13.3603 20.579 13.2197 20.7197C13.079 20.8603 13 21.0511 13 21.25C13 21.4489 13.079 21.6397 13.2197 21.7803C13.3603 21.921 13.5511 22 13.75 22H20.25C20.4489 22 20.6397 21.921 20.7803 21.7803C20.921 21.6397 21 21.4489 21 21.25C21 21.0511 20.921 20.8603 20.7803 20.7197C20.6397 20.579 20.4489 20.5 20.25 20.5H13.75Z" fill="url(#paint0_linear_1154_654)"/>
                                    <defs>
                                    <linearGradient id="paint0_linear_1154_654" x1="17" y1="9" x2="17" y2="25" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#71BF1E"/>
                                    <stop offset="1" stop-color="#71BF1E"/>
                                    </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <div class="info-text">${appointmentData.booking_person.notes}</div>
                        </div> `;
    
}

async function cancelAppointment(showMessage=true) {
    let appointmentId = sessionStorage.getItem("appointment_id");

    if (!appointmentId) {
        showToast("Error!", "No appointment found to cancel.", "danger-toast");
        return;
    }

    try {
        let headers = {"X-CSRFToken": getCookie("csrftoken")};
        let response = await fetch(`${API_BASE_URL}appointments/${appointmentId}`, {
            headers: headers,
            method: "DELETE"
        });

        if (response.ok) {
            if (showMessage) showToast("Success!", "Your appointment has been cancelled.", "success-toast");
            sessionStorage.removeItem("appointment_id");
            setTimeout(() => {
                window.location.href = "/book-appointments/"; 
            }, 1500);

        } else {
            showToast("Error!", "Failed to cancel appointment.", "danger-toast");
        }
    } catch (err) {
        console.error("Cancel Error:", err);
        showToast("Error!", "Something went wrong. Please try again.", "danger-toast");
    }
}



// Action handlers for second modal
function editInformation() {
    nextActionsModal.hide();
    isEditMode = true;
}


function saveToUserCalendar() {
  const appointmentData = {
    title: "Appointment Booking",
    description: "Your appointment with us.",
    location: "Lahore, Pakistan",
    start: "20250918T100000Z", // UTC format
    end: "20250918T110000Z"
  };

  const icsContent = `
BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
BEGIN:VEVENT
DTSTAMP:${appointmentData.start}
DTSTART:${appointmentData.start}
DTEND:${appointmentData.end}
SUMMARY:${appointmentData.title}
DESCRIPTION:${appointmentData.description}
LOCATION:${appointmentData.location}
END:VEVENT
END:VCALENDAR
`;

  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'appointment.ics';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}