
let principleId = JSON.parse(document.getElementById("principleId").textContent) || null;
let principle_data = null;
let selectedQuestionsByCategory = new Map();
window.addEventListener('load', get_principle_data());

async function get_principle_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}principles/${principleId}/categories/questions`, null, headers, 'GET');
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
    
    // Check if principle has any categories
    if (!data.categories || data.categories.length === 0) {
        const noDataDiv = document.createElement('div');
        noDataDiv.className = 'no-data-message';
        noDataDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Categories Available</h3>
                <p>This principle doesn't have any categories configured yet. Please check back later or contact support.</p>
            </div>
        `;
        container.appendChild(noDataDiv);
        return;
    }
    
    data.categories.forEach(category => {
        const accordionBox = document.createElement('div');
        accordionBox.className = 'accordian_box';
        const titleDiv = document.createElement('div');
        titleDiv.className = 'accordian_title';
        titleDiv.innerHTML = `<h4>${category.category.name}</h4>`;
        const contentDiv = document.createElement('div');
        contentDiv.className = 'accordian_cnt';
        // Check if category has any pest types or questions
        if (!category.pest_types || category.pest_types.length === 0) {
            const accordionBox = document.createElement('div');
            accordionBox.className = 'accordian_box';
            const titleDiv = document.createElement('div');
            titleDiv.className = 'accordian_title';
            titleDiv.innerHTML = `<h4>${category.category.name}</h4>`;
            
            const emptyContentDiv = document.createElement('div');
            emptyContentDiv.className = 'accordian_cnt empty-category';
            emptyContentDiv.innerHTML = `
                <div class="empty-category-message">
                    <img src="/static/img/info-circle.svg" alt="Info" style="width: 20px; height: 20px; opacity: 0.6;">
                    <span>No pest control measures available for this category</span>
                </div>
            `;
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(emptyContentDiv);
            container.appendChild(accordionBox);
            return;
        }
        
        const firstPestType = category.pest_types.find(pt => pt.questions.length > 0);
        
        // Check if there are any questions at all in this category
        const hasAnyQuestions = category.pest_types.some(pt => pt.questions && pt.questions.length > 0);
        if (!hasAnyQuestions) {
            const accordionBox = document.createElement('div');
            accordionBox.className = 'accordian_box';
            const titleDiv = document.createElement('div');
            titleDiv.className = 'accordian_title';
            titleDiv.innerHTML = `<h4>${category.category.name}</h4>`;
            
            const emptyContentDiv = document.createElement('div');
            emptyContentDiv.className = 'accordian_cnt empty-category';
            emptyContentDiv.innerHTML = `
                <div class="empty-category-message">
                    <img src="/static/img/info-circle.svg" alt="Info" style="width: 20px; height: 20px; opacity: 0.6;">
                    <span>No questions available for this category yet</span>
                </div>
            `;
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(emptyContentDiv);
            container.appendChild(accordionBox);
            return;
        }
        
        const firstQuestion = firstPestType?.questions[0]?.question?.text || '';
        const firstQuestionId = firstPestType?.questions[0]?.question?.id || null;
        const hasPestTypes = category.pest_types.some(pt => pt.pest_type !== null);
        
        if (hasPestTypes) {
            const pestType = category.pest_types.find(pt => pt.pest_type !== null);
            contentDiv.innerHTML = `
                <p>${pestType?.pest_type?.name || ''} 
                <img src="/static/img/right.svg" alt=""> 
                ${firstQuestion}</p>
                <img src="/static/img/down.svg" alt="">
            `;
        } else {
            contentDiv.innerHTML = `
                <p>${firstQuestion}</p>
                <img src="/static/img/down.svg" alt="">
            `;
        }
        
        const innerDiv = document.createElement('div');
        innerDiv.className = hasPestTypes ? 'accordian_inner pest_inner' : 'accordian_inner';
        const ul = document.createElement('ul');
        
        if (hasPestTypes) {
            category.pest_types.forEach((pestType, pestIndex) => {
                if (pestType.pest_type) {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <a href="#" class="question-link pest-type-link" data-pest-index="${pestIndex}">
                            ${pestType.pest_type.name} 
                            <img src="/static/img/arrow-right.svg" alt="">
                        </a>
                    `;
                    
                    if (pestType.questions.length > 0) {
                        const pestDropdown = document.createElement('ul');
                        pestDropdown.className = 'pest_dropdown';
                        // Initially hide all dropdowns except the first one
                        pestDropdown.style.display = pestIndex === 0 ? 'block' : 'none';
                        
                        pestType.questions.forEach(question => {
                            const questionLi = document.createElement('li');
                            questionLi.innerHTML = `
                                <label class="question-checkbox-label">
                                    <input type="checkbox" class="question-checkbox" data-question-id="${question.question.id}">
                                    <span class="question-text">${question.question.text}</span>
                                </label>
                            `;
                            pestDropdown.appendChild(questionLi);
                        });   
                        li.appendChild(pestDropdown);
                    } else {
                        // Show message if pest type has no questions
                        const pestDropdown = document.createElement('ul');
                        pestDropdown.className = 'pest_dropdown';
                        pestDropdown.style.display = pestIndex === 0 ? 'block' : 'none';
                        
                        const emptyQuestionLi = document.createElement('li');
                        emptyQuestionLi.className = 'empty-questions';
                        emptyQuestionLi.innerHTML = `
                            <div class="empty-questions-message">
                                <img src="/static/img/info-circle.svg" alt="Info" style="width: 16px; height: 16px; opacity: 0.6;">
                                <span>No questions available for ${pestType.pest_type.name}</span>
                            </div>
                        `;
                        pestDropdown.appendChild(emptyQuestionLi);
                        li.appendChild(pestDropdown);
                    }
                    ul.appendChild(li);
                }
            });
        } else {
            // Handle categories without pest types
            if (category.pest_types[0] && category.pest_types[0].questions.length > 0) {
                category.pest_types[0].questions.forEach(question => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <label class="question-checkbox-label">
                            <input type="checkbox" class="question-checkbox" data-question-id="${question.question.id}">
                            <span class="question-text">${question.question.text}</span>
                        </label>
                    `;
                    ul.appendChild(li);
                });
            } else {
                const emptyLi = document.createElement('li');
                emptyLi.className = 'empty-questions';
                emptyLi.innerHTML = `
                    <div class="empty-questions-message">
                        <img src="/static/img/info-circle.svg" alt="Info" style="width: 16px; height: 16px; opacity: 0.6;">
                        <span>No questions available for this category</span>
                    </div>
                `;
                ul.appendChild(emptyLi);
            }
        }
        innerDiv.appendChild(ul);
        const formContainer = document.createElement('div');
        formContainer.className = 'form-container';
        const firstQuestionData = firstPestType?.questions[0];
        const hasAnswer = firstQuestionData?.answer && 
                         (firstQuestionData.answer.details || 
                          (firstQuestionData.answer.images && firstQuestionData.answer.images.length > 0));
        
        if (hasAnswer) {
            formContainer.style.display = 'block';
            contentDiv.classList.add('active');
            innerDiv.style.display = 'block';
        } else {
            formContainer.style.display = 'block';
            innerDiv.style.display = 'block';
        }
        
        accordionBox.appendChild(titleDiv);
        accordionBox.appendChild(contentDiv);
        accordionBox.appendChild(innerDiv);
        accordionBox.appendChild(formContainer);
        container.appendChild(accordionBox);
        
        // Add pest type dropdown toggle functionality
        if (hasPestTypes) {
            const pestTypeLinks = accordionBox.querySelectorAll('.pest-type-link');
            pestTypeLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const pestIndex = parseInt(this.getAttribute('data-pest-index'));
                    
                    // Hide all dropdowns in this category
                    const allDropdowns = accordionBox.querySelectorAll('.pest_dropdown');
                    allDropdowns.forEach(dropdown => {
                        dropdown.style.display = 'none';
                    });
                    
                    // Show the clicked dropdown
                    const targetDropdown = allDropdowns[pestIndex];
                    if (targetDropdown) {
                        targetDropdown.style.display = 'block';
                    }
                    
                    // Update the content div to show the selected pest type and its first question
                    const selectedPestType = category.pest_types.filter(pt => pt.pest_type !== null)[pestIndex];
                    if (selectedPestType) {
                        const selectedFirstQuestion = selectedPestType?.questions[0]?.question?.text || 'No questions available';
                        contentDiv.innerHTML = `
                            <p>${selectedPestType?.pest_type?.name || ''} 
                            <img src="/static/img/right.svg" alt=""> 
                            ${selectedFirstQuestion}</p>
                            <img src="/static/img/down.svg" alt="">
                        `;
                    }
                });
            });
        }
        
        if (firstQuestionId) {
            const categoryId = category.category.id;
            if (!selectedQuestionsByCategory.has(categoryId)) {
                selectedQuestionsByCategory.set(categoryId, new Set());
            }
            
            const firstCheckbox = accordionBox.querySelector(`input[data-question-id="${firstQuestionId}"]`);
            if (firstCheckbox) {
                firstCheckbox.checked = true;
                selectedQuestionsByCategory.get(categoryId).add(firstQuestionId.toString());
                const selectedQs = contentDiv.querySelector("p");
                renderQuestionForm(formContainer, Array.from(selectedQuestionsByCategory.get(categoryId)), data, selectedQs);
            }
        }
    });
    
    // Show completion message if no categories were processed
    const processedCategories = container.querySelectorAll('.accordian_box');
    if (processedCategories.length === 0) {
        const noContentDiv = document.createElement('div');
        noContentDiv.className = 'no-content-message';
        noContentDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Content Available</h3>
                <p>All categories are empty or have no questions configured. Please contact support for assistance.</p>
            </div>
        `;
        container.appendChild(noContentDiv);
        return;
    }
    
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
        <span class="btn-text">Submit & Next</span>
    `;
    next_submit_button.addEventListener('click', handleGlobalSubmit);
    let buttons_container = document.createElement("div");
    buttons_container.classList.add("button-container");
    buttons_container.appendChild(previousButton);
    buttons_container.appendChild(next_submit_button);
    container.appendChild(buttons_container);    
    setupEventHandlers(data);
}

function navigateToStep(direction) {
    const menuItems = [...document.querySelectorAll('.side_menu ul li')];
    const activeIndex = menuItems.findIndex(li => li.classList.contains('active'));

    if (activeIndex === -1) return; // No active page found

    let targetIndex = activeIndex + (direction === 'next' ? 1 : -1);

    // Prevent going beyond range
    if (targetIndex < 0 || targetIndex >= menuItems.length) return;

    const targetLink = menuItems[targetIndex].querySelector('a');
    if (targetLink) {
        window.location.href = targetLink.getAttribute('href');
    }
}

function handlePrevious(event) {
    event.preventDefault();
    navigateToStep('prev');
}

async function handleGlobalSubmit(event) {
    event.preventDefault();
    const button = event.target.closest("button")
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl ? buttonTextEl.textContent : button.textContent;
    let allValid = true;
    let answersList = [];

    principle_data.categories.forEach(category => {
        let categoryId = category.category.id;
        let selectedQs = selectedQuestionsByCategory.get(categoryId) || new Set();

        if (selectedQs.size === 0) {
            showToast("Warning!", `Please answer at least one question in "${category.category.name}"`, "danger-toast");
            allValid = false;
            return;
        }

        const accordionBox = [...document.querySelectorAll('.accordian_box')]
            .find(box => box.querySelector('.accordian_title h4').textContent === category.category.name);
        if (accordionBox) {
            const form = accordionBox.querySelector('.details-form');
            if (!form) return;
            const formData = new FormData(form);
            const details = formData.get('details');
            const imageFiles = formData.getAll('images').filter(file => file.size > 0);
            const existingImages = [...form.querySelectorAll('.added_item[data-image-id]')]
                .map(item => item.getAttribute('data-image-id'));
            if (!details || (imageFiles.length === 0 && existingImages.length === 0)) {
                showToast("Warning!", `Please provide a comment and at least one image for "${category.category.name}"`, "danger-toast");
                allValid = false;
                return;
            }
            answersList.push({
                questionIds: Array.from(selectedQs),
                details,
                imageFiles,
                existingImages
            });
        }
    });
    if (!allValid) return;
    try {
        button.disabled = true;
        beforeLoad(button);
        for (const answer of answersList) {
            await saveQuestionDataGlobal(answer.questionIds, answer.details, answer.imageFiles, answer.existingImages);
        }
        setTimeout(() => {
            afterLoad(button, "Saved!");
            navigateToStep('next');
        }, 800);
    } catch (error) {
        console.error("Error in global submit:", error);
        afterLoad(button, originalButtonText);
        button.disabled = false;
        showToast("Error!", "Something went wrong while saving. Please try again.", "danger-toast");
    }
}

async function saveQuestionDataGlobal(questionIds, details, imageFiles, existingImages) {
    let headers = { 'X-CSRFToken': getCookie('csrftoken') };
    for (const questionId of questionIds) {
        try {
            const questionFormData = new FormData();
            questionFormData.append("question", questionId);
            questionFormData.append("details", details);
            const checkResponse = await requestAPI(`${API_BASE_URL}answers/by-question/${questionId}`, null, headers, 'GET');
            let answerId = null;
            let isUpdate = false;
            if (checkResponse.status == 200) {
                const answers = await checkResponse.json();
                if (answers.length > 0) {
                    answerId = answers[0].id;
                    isUpdate = true;
                }
            }
            let apiUrl = `${API_BASE_URL}answers`;
            let method = 'POST';
            if (isUpdate) {apiUrl = `${API_BASE_URL}answers/${answerId}`; method = 'PATCH';}
            let response = await requestAPI(apiUrl, questionFormData, headers, method);
            let responseData = await response.json();

            if (response.status === 201 || response.status === 200) {
                if (imageFiles.length > 0) {
                    let imageFormData = new FormData();
                    imageFiles.forEach(file => {
                        imageFormData.append('images', file);
                    });
                    await requestAPI(`${API_BASE_URL}answers/${responseData.data.id}/upload-images`, imageFormData, headers, 'POST');
                }
            } else {
                console.error(`Failed to save answer for question ${questionId}`);
            }
        } catch (err) {
            console.error(`Error saving answer for question ${questionId}:`, err);
        }
    }
}

function setupEventHandlers(data) {
    $(".accordian_cnt").click(function() {
        $(this).toggleClass("active").next().slideToggle();
    });
    
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('question-checkbox')) {
            const questionId = e.target.getAttribute('data-question-id');
            const accordionBox = e.target.closest('.accordian_box');
            const formContainer = accordionBox.querySelector('.form-container');
            const contentDiv = accordionBox.querySelector('.accordian_cnt');
            const selectedQs = contentDiv.querySelector("p");
            const categoryElement = accordionBox.querySelector('.accordian_title h4');
            const categoryName = categoryElement.textContent;
            
            let categoryId = null;
            data.categories.forEach(cat => {
                if (cat.category.name === categoryName) {
                    categoryId = cat.category.id;
                }
            });
            
            if (!categoryId) return;
            if (!selectedQuestionsByCategory.has(categoryId)) {
                selectedQuestionsByCategory.set(categoryId, new Set());
            }
            
            const categorySelections = selectedQuestionsByCategory.get(categoryId);
            
            if (e.target.checked) {
                categorySelections.add(questionId);
            } else {
                categorySelections.delete(questionId);
            }
            
            // Ensure the accordion is open
            if (!contentDiv.classList.contains('active')) {
                contentDiv.click();
            }
            
            // Get selected questions from current category only
            const currentCategoryQuestions = Array.from(categorySelections);
            
            if (currentCategoryQuestions.length > 0) {
                formContainer.style.display = 'block';
                updateSelectedQuestionDisplay(selectedQs, currentCategoryQuestions, data);
                renderQuestionForm(formContainer, currentCategoryQuestions, data, selectedQs);
            } else {
                formContainer.style.display = 'none';
                formContainer.innerHTML = '';
            }
        }
    });
}

function updateSelectedQuestionDisplay(selectedQs, questionIds, data) {
    if (questionIds.length === 1) {
        // Single question - show the question text
        let questionData = findQuestionById(questionIds[0], data);
        selectedQs.textContent = questionData ? questionData.text : '';
    } else if (questionIds.length > 1) {
        // Multiple questions - show count
        selectedQs.textContent = `${questionIds.length} questions selected`;
    }
}

function findQuestionById(questionId, data) {
    let questionData = null;
    data.categories.forEach(category => {
        category.pest_types.forEach(pestType => {
            pestType.questions.forEach(question => {
                if (question.question.id.toString() === questionId) {
                    questionData = question.question;
                }
            });
        });
    });
    return questionData;
}

function renderQuestionForm(container, questionIds, data, selectedQs) {
    const questions = [];
    let answerData = null;
    
    // Collect question data and find existing answer data
    questionIds.forEach(questionId => {
        data.categories.forEach(category => {
            category.pest_types.forEach(pestType => {
                pestType.questions.forEach(question => {
                    if (question.question.id.toString() === questionId) {
                        questions.push(question.question);
                        // Use the first available answer data as template
                        if (!answerData && question.answer) {
                            answerData = question.answer;
                        }
                    }
                });
            });
        });
    });

    if (questions.length === 0) {
        console.error('No question data found for IDs:', questionIds);
        return;
    }

    let formHTML = `
        <div class="accordion_selected">
            <div class="template_title">
                <h4>${questionIds.length === 1 ? 'Fill your details below' : `Answer for ${questionIds.length} selected questions`}</h4>
                <a href="#" class="save-btn hide">Save Info</a>
            </div>
    `;
    
    // Show selected questions list if multiple
    if (questionIds.length > 1) {
        formHTML += `
            <div class="selected-questions-info">
                <p><strong>This answer will be applied to all selected questions:</strong></p>
                <ul class="selected-questions-list">
        `;
        questions.forEach(question => {
            formHTML += `<li>${question.text}</li>`;
        });
        formHTML += `
                </ul>
            </div>
        `;
    }
    
    formHTML += `
            <form class="details-form" data-question-ids="${questionIds.join(',')}">
                <div class="row">
                    <div class="col-md-12">
                        <div class="inform_item">
                            <label>Comment</label>
                            <textarea name="details" placeholder="Description">${answerData?.details || ''}</textarea>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="inform_item">
                            <label>Images</label>
                        </div>
                        <div class="add_wraper">
                            <div class="add_box">
                                <label class="custom-upload">
                                    <input type="file" name="images" multiple class="image-upload" />
                                    <img src="/static/img/download.svg" alt="">
                                    Add Image
                                </label>
                            </div>
                            <div class="image-preview-container">
    `;
    
    if (answerData?.images?.length > 0) {
        answerData.images.forEach(image => {
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
    
    // Add event listeners
    container.querySelector('.image-upload').addEventListener('change', function(e) {
        handleImageUpload(e, container);
    });
    
    container.querySelector('.save-btn').addEventListener('click', function(e) {
        e.preventDefault();
        let container = this.closest(".accordion_selected");
        saveQuestionData(container, questionIds);
    });
    
    container.querySelectorAll('.delete_icon a').forEach(deleteBtn => {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const imageId = this.closest(".added_item").getAttribute("data-image-id");
            delete_answer_image(imageId);
        });
    });
}

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