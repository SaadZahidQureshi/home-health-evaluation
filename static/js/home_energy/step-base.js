let principleId = JSON.parse(document.getElementById("principleId").textContent) || null;
let principle_data = null;
let selectedQuestionsByGroup = new Map();
let questionsWithInitialAnswers = new Set();
let customer_id = sessionStorage.getItem("customer_id") || null;
window.addEventListener('load', () =>{
    get_principle_data(),
    get_principle_status_data()
});

async function get_principle_status_data() {
    let customer_id = sessionStorage.getItem("customer_id") || null;
    try {
        let headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        };

        let endpoint = `${API_BASE_URL}steps/status`;
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
    if (!container) return;

    data.forEach(item => {
        let el = container.querySelector(`li[data-order="${item.order}"]`);
        if (el) {
            el.classList.remove("completed", "pending");
            if (item.status) {
                el.classList.add(item.status);
            }
        }
    });
}

async function get_principle_data() {
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let enndpoint = `${API_BASE_URL}steps/${principleId}/questions`
        if (customer_id) enndpoint = `${API_BASE_URL}steps/${principleId}/questions?customer_id=${customer_id}`
        let response = await requestAPI(enndpoint, null, headers, 'GET');
        response.json().then(function(res) {
            if (response.status == 200) {
                principle_data = res;
                render_principle_data(principle_data);
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


function render_principle_data(data) {
    let container = document.querySelector(".right-mainpart");
    container.innerHTML = '';
    
    if (!data.groups || data.groups.length === 0) {
        const noDataDiv = document.createElement('div');
        noDataDiv.className = 'no-data-message';
        noDataDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Groups Available</h3>
                <p>This principle doesn't have any groups configured yet. Please check back later or contact support.</p>
            </div>
        `;
        container.appendChild(noDataDiv);
        return;
    }
    
    data.groups.forEach((group, index) => {
        const accordionBox = document.createElement('div');
        accordionBox.className = 'accordian_box';
        accordionBox.setAttribute("data-group", group.id);

        if (isLastStep()) {
            let finalDiv = document.createElement('form');
            finalDiv.className = 'inform_item';
            finalDiv.classList.add("details-form")
            finalDiv.innerHTML = `<textarea name="details" placeholder="Remarks">${group?.feedback?.text || ""}</textarea>`
            
            let titleDiv = document.createElement("div");
            titleDiv.className = 'accordian_title';
            titleDiv.innerHTML = `<h4>${group.questions[0].text}</h4>`
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(finalDiv);
            container.appendChild(accordionBox);
            return;
        }

        if (group.questions && group.questions.length > 0) {
            group.questions.forEach(question => {
                let questionDiv = document.createElement("div");
                questionDiv.className = 'col-md-12';
                questionDiv.style.marginBottom = "1.5rem";

                let titleDiv = document.createElement("div");
                titleDiv.className = 'accordian_title';
                titleDiv.innerHTML = `<h4>${question.text}</h4>`

                questionDiv.appendChild(titleDiv);
                
                if (question.field_type === 'dropdown' && question.options && question.options.length > 0) {
                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'accordian_cnt';

                    contentDiv.innerHTML = `
                        <p>Select Options</p>
                        <img src="/static/img/down.svg" alt="">
                    `;

                    const innerDiv = document.createElement('div');
                    innerDiv.className = 'accordian_inner';
                    
                    const ul = document.createElement("ul");
                    question.options.forEach(option => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <label class="question-checkbox-label">
                                <input type="checkbox" class="question-checkbox" 
                                    value="${option.id}" name="dropdown_question_${question.id}"
                                    data-question-id="${question.id}"
                                    ${option.is_selected ? 'checked' : ''}>
                                <span class="question-text">${option.text}</span>
                            </label>
                        `;
                        ul.appendChild(li);
                    })
                    innerDiv.appendChild(ul);
                    questionDiv.appendChild(contentDiv);
                    questionDiv.appendChild(innerDiv);
                } else {
                    let innerContentDiv = document.createElement("div");
                    innerContentDiv.className = 'inform_item';
                    innerContentDiv.innerHTML = `
                        <input type="${question.field_type}" name="text" data-question-id="${question.id}" value="${question?.answer?.text || ''}" placeholder="Write..." />
                    `;
                    questionDiv.appendChild(innerContentDiv);
                }
                accordionBox.appendChild(questionDiv);
            });
            
            const formContainer = document.createElement('div');
            formContainer.className = 'form-container';
            formContainer.style.display = 'block';
            accordionBox.appendChild(formContainer);
            container.appendChild(accordionBox);
            
            const groupId = group.id;
            if (!selectedQuestionsByGroup.has(groupId)) {
                selectedQuestionsByGroup.set(groupId, new Set());
            }
            
            // Initialize selected questions
            group.questions.forEach(question => {
                if (question.field_type === 'dropdown' && question.options) {
                    question.options.forEach(option => {
                        if (option.is_selected) {
                            selectedQuestionsByGroup.get(groupId).add(`${question.id}_${option.id}`);
                            questionsWithInitialAnswers.add(question.id.toString());
                        }
                    });
                } else if (question.answer) {
                    // selectedQuestionsByGroup.get(groupId).add(question.id.toString());
                    questionsWithInitialAnswers.add(question.id.toString());
                }
            });
            
            renderQuestionForm(formContainer, group, data);
            
        } else {
            contentDiv.innerHTML = `
                <p>No questions available</p>
                <img src="/static/img/down.svg" alt="">
            `;
            
            const innerDiv = document.createElement('div');
            innerDiv.className = 'accordian_inner empty-group';
            innerDiv.innerHTML = `
                <div class="empty-group-message">
                    <span>No questions available for this group</span>
                </div>
            `;
            
            const formContainer = document.createElement('div');
            formContainer.className = 'form-container';
            formContainer.style.display = 'block';
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(contentDiv);
            accordionBox.appendChild(innerDiv);
            accordionBox.appendChild(formContainer);
            container.appendChild(accordionBox);
            
            renderQuestionForm(formContainer, group, data);
        }
    });
    
    const previousButton = document.createElement('button');
    previousButton.type = "button";
    previousButton.innerHTML = `
        <span class="spinner-border hide" role="status" aria-hidden="true"></span>
        <span class="btn-text">Previous</span>
    `;
    previousButton.addEventListener('click', handlePrevious);
    
    const next_submit_button = document.createElement('button');
    next_submit_button.type = "button";
    next_submit_button.innerHTML = `
        <span class="spinner-border hide" role="status" aria-hidden="true"></span>
        <span class="btn-text">${!isLastStep ? "Submit & Next" : "Submit" }</span>
    `;
    next_submit_button.addEventListener('click', handleGlobalSubmit);
    
    let buttons_container = document.createElement("div");
    buttons_container.classList.add("button-container");
    buttons_container.appendChild(previousButton);
    buttons_container.appendChild(next_submit_button);
    container.appendChild(buttons_container);
    
    setupEventHandlers(data);
}

function setupEventHandlers(data) {
    $(".accordian_cnt").click(function() {
        $(this).toggleClass("active").next().slideToggle();
    });
    
    questionsWithInitialAnswers.clear();
    
    // Collect initial answers
    data.groups.forEach(group => {
        group.questions.forEach(question => {
            if (question.field_type === 'dropdown' && question.options) {
                question.options.forEach(option => {
                    if (option.is_selected) {
                        questionsWithInitialAnswers.add(`${question.id}_${option.id}`);
                    }
                });
            } else if (question.answer) {
                questionsWithInitialAnswers.add(question.id.toString());
            }
        });
    });
    
    // Initialize selections
    data.groups.forEach(group => {
        if (!selectedQuestionsByGroup.has(group.id)) {
            selectedQuestionsByGroup.set(group.id, new Set());
        }
        
        group.questions.forEach(question => {
            if (question.field_type === 'dropdown' && question.options) {
                question.options.forEach(option => {
                    if (option.is_selected) {
                        selectedQuestionsByGroup.get(group.id).add(`${question.id}_${option.id}`);
                    }
                });
            }
        });
    });
    
    // Update accordion content counts
    data.groups.forEach(group => {
        const accordionBox = document.querySelector(`[data-group-id="${group.id}"]`)?.closest('.accordian_box');
        if (!accordionBox) return;
        
        const contentDiv = accordionBox.querySelector('.accordian_cnt');
        const contentP = contentDiv?.querySelector('p');
        
        if (contentP) {
            updateAccordionContentCount(group, contentP);
        }
    });
    
    // Handle dropdown and input changes
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('question-dropdown')) {
            handleDropdownChange(e.target, data);
        } else if (e.target.classList.contains('question-input')) {
            handleTextInputChange(e.target, data);
        }
    });
}

function handleDropdownChange(dropdown, data) {
    const questionId = dropdown.getAttribute('data-question-id');
    const groupId = parseInt(dropdown.getAttribute('data-group-id'));
    const accordionBox = dropdown.closest('.accordian_box');
    const contentDiv = accordionBox.querySelector('.accordian_cnt');
    const contentP = contentDiv.querySelector('p');
    
    if (!selectedQuestionsByGroup.has(groupId)) {
        selectedQuestionsByGroup.set(groupId, new Set());
    }
    
    const groupSelections = selectedQuestionsByGroup.get(groupId);
    
    if (dropdown.value) {
        groupSelections.add(questionId);
    } else {
        groupSelections.delete(questionId);
        
        if (questionsWithInitialAnswers.has(questionId)) {
            if (!window.questionsToDelete) {
                window.questionsToDelete = new Set();
            }
            window.questionsToDelete.add(questionId);
        }
    }
    
    const group = data.groups.find(g => g.id === groupId);
    if (group && contentP) {
        updateAccordionContentCount(group, contentP);
    }
    
    if (!contentDiv.classList.contains('active')) {
        contentDiv.click();
    }
}

function handleTextInputChange(input, data) {
    const questionId = input.getAttribute('data-question-id');
    const groupId = parseInt(input.getAttribute('data-group-id'));
    const accordionBox = input.closest('.accordian_box');
    const contentDiv = accordionBox.querySelector('.accordian_cnt');
    const contentP = contentDiv.querySelector('p');
    
    if (!selectedQuestionsByGroup.has(groupId)) {
        selectedQuestionsByGroup.set(groupId, new Set());
    }
    
    const groupSelections = selectedQuestionsByGroup.get(groupId);
    
    if (input.value.trim()) {
        groupSelections.add(questionId);
    } else {
        groupSelections.delete(questionId);
        
        if (questionsWithInitialAnswers.has(questionId)) {
            if (!window.questionsToDelete) {
                window.questionsToDelete = new Set();
            }
            window.questionsToDelete.add(questionId);
        }
    }
    
    const group = data.groups.find(g => g.id === groupId);
    if (group && contentP) {
        updateAccordionContentCount(group, contentP);
    }
}

function countSelectedQuestions(group) {
    const groupSelections = selectedQuestionsByGroup.get(group.id);
    if (!groupSelections) return 0;
    return groupSelections.size;
}

function updateAccordionContentCount(group, contentP) {
    if (!contentP) return;
    
    const selectedCount = countSelectedQuestions(group);
    
    if (selectedCount > 0) {
        const countText = `${selectedCount} option${selectedCount > 1 ? 's' : ''} selected`;
        contentP.innerHTML = countText;
    } else {
        contentP.innerHTML = 'Select options';
    }
}

function renderQuestionForm(container, group, data, preservedDetails = '', preservedImages = []) {
    let answerData = null;
    if (group && group.feedback) {
        answerData = {
            details: group.feedback.text,
            images: group.feedback.images
        };
    }

    const detailsToUse = preservedDetails || answerData?.details || '';
    const imagesToUse = preservedImages.length > 0 ? preservedImages : (answerData?.images || []);

    let formHTML = `
        <div class="accordion_selected">
            <div class="template_title">
                <h4>Fill your feedback below</h4>
            </div>
            <form class="details-form" data-group-id="${group.id}">
                <div class="row">
                    <div class="col-md-12">
                        <div class="inform_item">
                            <label>Comment</label>
                            <textarea name="details" placeholder="Description">${detailsToUse}</textarea>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="inform_item">
                            <label>Images</label>
                        </div>
                        <div class="add_wraper">
                            <div class="add_box">
                                <label class="custom-upload">
                                    <input type="file" name="images" multiple class="image-upload" accept="image/jpeg, image/jpg, image/png"/>
                                    <img src="/static/img/download.svg" alt="">
                                    Add Image
                                </label>
                            </div>
                            <div class="image-preview-container">
    `;
    
    if (imagesToUse.length > 0) {
        imagesToUse.forEach(image => {
            if (image.id) {
                // Database image
                formHTML += `
                    <div class="added_item" data-image-id="${image.id}">
                        <div class="added_image">
                            <img src="${image.image}" alt="">
                        </div>
                        <div class="delete_icon">
                            <a href="#"><img src="/static/img/delete.svg" alt=""></a>
                        </div>
                    </div>
                `;
            } else {
                // Preview image
                formHTML += `
                    <div class="added_item">
                        <div class="added_image">
                            <img src="${image.src}" alt="">
                        </div>
                        <div class="delete_icon">
                            <a href="#"><img src="/static/img/delete.svg" alt=""></a>
                        </div>
                    </div>
                `;
            }
        });
    }
    
    formHTML += `
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    `;
    
    container.innerHTML = formHTML;
    
    const imageUpload = container.querySelector('.image-upload');
    if (imageUpload) {
        imageUpload.addEventListener('change', function(e) {
            handleImageUpload(e, container);
        });
    }
    
    container.querySelectorAll('.delete_icon a').forEach(deleteBtn => {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const imageId = this.closest(".added_item").getAttribute("data-image-id");
            delete_answer_image(imageId);
        });
    });
}

let selectedFiles = {};

function handleImageUpload(event, container) {
    const files = Array.from(event.target.files).filter(file => file.size > 0);
    const previewContainer = container.querySelector('.image-preview-container');
    
    if (files.length === 0) {
        showToast("Warning!", "Please select valid image files", "danger-toast");
        return;
    }

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewItem = document.createElement('div');
            previewItem.className = 'added_item';
            previewItem.innerHTML = `
                <div class="added_image">
                    <img src="${e.target.result}" alt="">
                </div>
                <div class="delete_icon">
                    <a href="#"><img src="/static/img/delete.svg" alt=""></a>
                </div>
            `;
            previewContainer.appendChild(previewItem);
            
            const groupId = container.querySelector('.details-form').getAttribute('data-group-id');
            if (!selectedFiles[groupId]) {
                selectedFiles[groupId] = [];
            }
            selectedFiles[groupId].push(file);
            
            previewItem.querySelector('.delete_icon a').addEventListener('click', function(e) {
                e.preventDefault();
                previewItem.remove();
            });
        };
        
        reader.readAsDataURL(file);
    }
}

async function delete_answer_image(imageId){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}photos/${imageId}`, null, headers, 'DELETE');
        if (response.status == 204) {
            showToast("Success", `Image deleted successfully!`, "success-toast");
            get_principle_data()
        }
        else{
            let responseData = await response.json();
            let errors = extractErrorMessages(responseData);
            showToast("Warning!", errors[0] || `Failed to delete`, "danger-toast");
        }
    }
    catch (err) {
        console.error(err);
        showToast("Error!", "An error occurred while deleting", "danger-toast");
    }
}


function isLastStep() {
    const menuItems = [...document.querySelectorAll('.side_menu ul li')];
    const activeIndex = menuItems.findIndex(li => li.classList.contains('active'));
    return activeIndex === menuItems.length - 1;
}


function handlePrevious(event) {
    event.preventDefault();
    navigateToStep('prev');
}


function navigateToStep(direction) {
    const menuItems = [...document.querySelectorAll('.side_menu ul li')];
    const activeIndex = menuItems.findIndex(li => li.classList.contains('active'));

    if (activeIndex === -1) return;

    let targetIndex = activeIndex + (direction === 'next' ? 1 : -1);

    if (targetIndex < 0 || targetIndex >= menuItems.length) return;

    const targetLink = menuItems[targetIndex].querySelector('a');
    if (targetLink) {
        window.location.href = targetLink.getAttribute('href');
    }
}


async function handleGlobalSubmit(event) {
    event.preventDefault();
    const button = event.target.closest("button");
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl ? buttonTextEl.textContent : button.textContent;

    beforeLoad(button);

    try {
        if (window.feedbacksToDelete && window.feedbacksToDelete.size > 0) {
            for (const categoryId of window.feedbacksToDelete) {
                const category = principle_data.groups.find(cat => cat.id === categoryId);
                if (category && category.feedback && category.feedback.id) {
                    await deleteFeedback(category.feedback.id);
                }
            }
            window.feedbacksToDelete.clear();
        }

        try {
            // Ensure customer_id exists
            if (!customer_id) {
                const customerResponse = await createCustomer();
                if (!customerResponse) {
                    throw new Error("Failed to create customer");
                }
                customer_id = customerResponse.id;
                sessionStorage.setItem("customer_id", customer_id);
            }
            
            let headers = {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie('csrftoken')
            };

            // Process each group
            for (const group of principle_data.groups) {
                // Handle questions
                if (group.questions && group.questions.length > 0) {
                    for (const question of group.questions) {
                        if (question.field_type === 'dropdown') {
                            // Get selected options
                            const checkboxes = document.querySelectorAll(`input[name="dropdown_question_${question.id}"]:checked`);
                            const selectedOptions = Array.from(checkboxes).map(cb => parseInt(cb.value));
                            
                            if (selectedOptions.length > 0) {
                                const response = await requestAPI(`${API_BASE_URL}question/${question.id}/selection`, JSON.stringify({customer_id: customer_id, selected_options: selectedOptions}), headers, 'POST');
                                if (response.status !== 200 && response.status !== 201) {
                                    throw new Error(`Failed to save selection for question ${question.id}`);
                                }
                            }
                        } else {
                            // Handle text inputs
                            const input = document.querySelector(`input[data-question-id="${question.id}"]`);
                            if (input && input.value.trim()) {
                                const response = await requestAPI(`${API_BASE_URL}question/${question.id}/answer`, JSON.stringify({text: input.value.trim(), customer_id: customer_id }), headers, 'POST');
                                if (response.status !== 200 && response.status !== 201) {
                                    throw new Error(`Failed to save answer for question ${question.id}`);
                                }
                            }
                        }
                    }
                }
                
                // Handle group feedback text
                const accordianBox = document.querySelector(`div[data-group="${group.id}"]`);
                if (accordianBox) {
                    const textarea = accordianBox.querySelector('textarea[name="details"]');
                    const imageFiles = selectedFiles[group.id] || [];
                    const existingImages = [...accordianBox.querySelectorAll('.added_item[data-image-id]')]
                        .map(item => item.getAttribute('data-image-id'));

                    // Save feedback text
                    if (textarea && textarea.value.trim()) {
                        const response = await requestAPI(`${API_BASE_URL}question-group/${group.id}/feedback?customer_id=${customer_id}`, JSON.stringify({customer_id: customer_id, text: textarea.value.trim() }), headers, 'POST');
                        if (response.status !== 200 && response.status !== 201) {
                            throw new Error(`Failed to save feedback for group ${group.id}`);
                        }
                    }

                    // Upload images
                    if (imageFiles.length > 0) {
                        const formData = new FormData();
                        formData.append('customer_id', customer_id);
                        imageFiles.forEach(image => {
                            formData.append('images', image);
                        });
                        
                        const imageHeaders = { 'X-CSRFToken': getCookie('csrftoken') };
                        
                        const response = await requestAPI(`${API_BASE_URL}question-group/${group.id}/upload-images`, formData, imageHeaders, 'POST');
                        if (response.status !== 200 && response.status !== 201) {
                            throw new Error(`Failed to upload images for group ${group.id}`);
                        }
                    }
                }
            }

            if (isLastStep()) {
                await new Promise(resolve => setTimeout(resolve, 2000));
                afterLoad(button, originalButtonText);
                showCustomerUpdateModal();
            } else {
                setTimeout(() => {
                    afterLoad(button, "Saved!");
                    navigateToStep('next');
                }, 800);
            }
            
            console.log('Form submitted successfully');
            
        } catch (error) {
            console.error('Error submitting form:', error);
            return false;
        }

    } catch (error) {
        console.error("Error in global submit:", error);
        afterLoad(button, originalButtonText);
        button.disabled = false;
        showToast("Error!", error.message || "Something went wrong while saving. Please try again.", "danger-toast");
    }
}


async function showCustomerUpdateModal() {
    const customer_id = sessionStorage.getItem("customer_id");
    if (!customer_id) {
        showToast("Error!", "Customer ID not found", "danger-toast");
        return;
    }
    const customerData = await getCustomerDetails(customer_id);
    if (!customerData) {
        showToast("Error!", "Failed to load customer details", "danger-toast");
        return;
    }
    let modalId = "addUserModal";
    let modal_el = document.getElementById(modalId);
    if (!modal_el) {
        modal_el = document.getElementById(modalId);
    }
    const form = modal_el.querySelector("form");

    form.querySelector('input[name="name"]').value = customerData.user.name || '';
    form.querySelector('input[name="email"]').value = customerData.user.email || '';
    form.querySelector('input[name="address"]').value = customerData.address || '';
    form.querySelector('input[name="city"]').value = customerData.city || '';
    form.querySelector('input[name="state"]').value = customerData.state || '';
    form.querySelector('input[name="zip"]').value = customerData.zip || '';

    if (customerData.house_image) {
        const imgElement = modal_el.querySelector('#id_image_preview');
        imgElement.src = customerData.house_image;
        imgElement.classList.remove("hide");
    }

    form.setAttribute("onsubmit", "updateCustomerInfo(event)")
    const modal = new bootstrap.Modal(modal_el);
    modal._element.addEventListener('hidden.bs.modal', function() {
        form.reset();
        form.removeAttribute("onsubmit")
        const imgElement = modal_el.querySelector('#id_image_preview');
        imgElement.classList.add("hide");
        imgElement.src = '';
    });
    modal.show();
}


async function updateCustomerInfo(event) {
    event.preventDefault()
    let form  = event.target;
    const formData = new FormData(form);
    const updateButton = document.querySelector(`button[form='${form.id}']`);

    const customer_id = sessionStorage.getItem("customer_id");
    if (!customer_id) {
        showToast("Error!", "Customer ID not found", "danger-toast");
        return;
    }
    
    // Validate required fields
    const name = formData.get('name');
    const email = formData.get('email');
    const address = formData.get('address');
    const city = formData.get('city');
    const state = formData.get('state');
    const zip = formData.get('zip');
    const house_image = formData.get('house_image');
    
    if (!name || !email || !address || !city || !state || !zip || !house_image) {
        showToast("Warning!", "Please fill all required fields", "danger-toast");
        return;
    }

    beforeLoad(updateButton)
    try {
        let headers = {'X-CSRFToken': getCookie('csrftoken')};
        let response = await requestAPI(`${API_BASE_URL}customers/residential-home/${customer_id}`, formData, headers, 'PATCH');
        if (response.status == 200) {
            afterLoad(updateButton, "Saved");
            const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            modal.hide();
            setTimeout(() => {
                successModal();
            }, 500);
            showToast("Success!", "Customer information updated successfully!", "success-toast");
        } else {
            let responseData = await response.json();
            afterLoad(updateButton, "Save");
            let errors = extractErrorMessages(responseData);
            showToast("Warning!", errors[0] || "Failed to update customer", "danger-toast");
        }
    } catch (err) {
        afterLoad(updateButton, "Save");
        console.error('Error updating customer:', err);
        showToast("Error!", "An error occurred while updating customer information", "danger-toast");
    } finally {
        afterLoad(updateButton, "Save");
    }
}


async function getCustomerDetails(customerId) {
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}customers/residential-home/${customerId}`, null, headers, 'GET');
        if (response.status == 200) {
            const customerData = await response.json();
            return customerData.data;
        } else {
            console.error('Failed to get customer details');
            return null;
        }
    } catch (err) {
        console.error('Error getting customer details:', err);
        return null;
    }
}


async function saveQuestionGroupFeedback(categoryId, details, imageFiles, existingImages) {
    const headers = { 
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
    };

    try {
        if (!customer_id) {
            const customerResponse = await createCustomer();
            if (!customerResponse) {
                throw new Error("Failed to create customer");
            }
            customer_id = customerResponse.id;
            sessionStorage.setItem("customer_id", customer_id);
        }

        const feedbackResponse = await requestAPI(
            `${API_BASE_URL}question-group/${categoryId}/feedback`,
            JSON.stringify({
                customer_id: customer_id,
                text: details
            }),
            headers,
            'POST'
        );

        if (!feedbackResponse.ok) {
            console.error(`Failed to save feedback for category ${categoryId}`);
            return false;
        }

        if (imageFiles.length > 0) {
            const imageFormData = new FormData();
            imageFiles.forEach(file => imageFormData.append('images', file));
            imageFormData.append('customer_id', customer_id);

            const imageHeaders = { 'X-CSRFToken': getCookie('csrftoken') };
            const imageResponse = await requestAPI(`${API_BASE_URL}question-group/${categoryId}/upload-images`, imageFormData, imageHeaders, 'POST');
            if (!imageResponse.ok) {
                console.error(`Failed to upload images for category ${categoryId}`);
                return false;
            }
            selectedFiles = [];
        }

        return true;
    } catch (err) {
        console.error(`Error saving feedback for category ${categoryId}:`, err);
        return false;
    }
}


async function deleteFeedback(feedbackId) {
    try {
        const headers = {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        };

        const response = await requestAPI(
            `${API_BASE_URL}feedbacks/${feedbackId}`,
            null,
            headers,
            'DELETE'
        );

        if (!response.ok) {
            console.error(`Failed to delete feedback ${feedbackId}`);
            return false;
        }

        return true;
    } catch (err) {
        console.error(`Error deleting feedback ${feedbackId}:`, err);
        return false;
    }
}


async function createCustomer() {
    try {
        const headers = {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        };
        
        const userResponse = await requestAPI(`${API_BASE_URL}user/me`, null, headers, 'GET');
        if (!userResponse.ok) {
            throw new Error("Failed to get current user info");
        }
        
        const userData = await userResponse.json();
        const createdById = userData.id;

        const response = await requestAPI(`${API_BASE_URL}customers/residential-home`, JSON.stringify({}), headers, 'POST');

        if (response.ok) {
            const customerData = await response.json();
            return customerData;
        } else {
            const errorData = await response.json();
            throw new Error(errorData.message || "Failed to create customer");
        }
    } catch (err) {
        console.error("Error creating customer:", err);
        showToast("Error!", "Failed to create customer record. Please try again.", "danger-toast");
        return null;
    }
}