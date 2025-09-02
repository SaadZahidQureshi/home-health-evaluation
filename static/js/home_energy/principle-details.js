
let principleId = JSON.parse(document.getElementById("principleId").textContent) || null;
let principle_data = null;
let selectedQuestionsByCategory = new Map();
let customer_id = sessionStorage.getItem("customer_id") || null;
window.addEventListener('load', get_principle_data());

async function get_principle_data(){
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
    
    // Check if step has any groups
    if (!data.groups || data.groups.length === 0) {
        const noDataDiv = document.createElement('div');
        noDataDiv.className = 'no-data-message';
        noDataDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Questions Available</h3>
                <p>This step doesn't have any question configured yet. Please check back later or contact support.</p>
            </div>
        `;
        container.appendChild(noDataDiv);
        return;
    }

    // Process each group
    data.groups.forEach(group => {
        // Create group card
        const groupCard = document.createElement('div');
        groupCard.className = 'category-card';
        
        // Group title only (no status)
        const groupTitle = document.createElement('h3');
        groupTitle.className = 'category-title';
        groupTitle.textContent = `Group #${group.id}`;
        // groupCard.appendChild(groupTitle);
        
        // Render questions for this group
        if (group.questions && group.questions.length > 0) {
            group.questions.forEach(question => {
                const questionSection = renderQuestion(question);
                groupCard.appendChild(questionSection);
            });
        }
        
        // Render group feedback if exists
        if (group.feedback) {
            const feedbackSection = renderFeedbackSection(group.feedback);
            groupCard.appendChild(feedbackSection);
        }
        
        container.appendChild(groupCard);
    });
    
    // Show message if no groups were processed
    const processedGroups = container.querySelectorAll('.category-card');
    if (processedGroups.length === 0) {
        const noContentDiv = document.createElement('div');
        noContentDiv.className = 'no-content-message';
        noContentDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Content Available</h3>
                <p>No groups found. Please check back later.</p>
            </div>
        `;
        container.appendChild(noContentDiv);
    }
}

// Helper function to render individual question
function renderQuestion(question) {
    const questionContainer = document.createElement('div');
    questionContainer.className = 'subcategory-section';
    
    // Question header
    const questionHeader = document.createElement('div');
    questionHeader.className = 'subcategory-header';
    questionHeader.innerHTML = `<strong>${question.text}</strong>`;
    questionContainer.appendChild(questionHeader);
    
    // Answer text
    if (question.answer && question.answer.text) {
        const answerContent = document.createElement('div');
        answerContent.className = 'feedback-note';
        answerContent.innerHTML = question.answer.text;
        questionContainer.appendChild(answerContent);
    }
    
    // Selected options (for dropdowns)
    if (question.options && question.options.length > 0) {
        const selectedOptions = question.options.filter(option => option.is_selected);
        if (selectedOptions.length > 0) {
            const optionsSection = renderOptionsSection(selectedOptions, 'Selected Options');
            questionContainer.appendChild(optionsSection);
        }
    }
    
    return questionContainer;
}

// Helper function to render options section
function renderOptionsSection(options, headerText = 'Selected Options') {
    if (options.length === 0) {
        return null;
    }
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-section';
    
    const optionsHeader = document.createElement('div');
    optionsHeader.className = 'section-header';
    optionsHeader.innerHTML = `<strong>${headerText}</strong>`;
    // optionsContainer.appendChild(optionsHeader);
    
    const optionsList = document.createElement('div');
    optionsList.className = 'options-list';
    
    options.forEach(option => {
        const optionItem = document.createElement('div');
        optionItem.className = 'option-item selected';
        optionItem.innerHTML = `
            <span class="option-indicator">✓</span>
            <span class="option-text">${option.text}</span>
        `;
        optionsList.appendChild(optionItem);
    });
    
    optionsContainer.appendChild(optionsList);
    return optionsContainer;
}

// Helper function to render feedback section
function renderFeedbackSection(feedback) {
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-section';
    
    // Feedback text
    if (feedback.text) {
        const noteHeader = document.createElement('div');
        noteHeader.className = 'section-header';
        noteHeader.innerHTML = '<strong>Comments</strong>';
        feedbackContainer.appendChild(noteHeader);
        
        const noteContent = document.createElement('div');
        noteContent.className = 'feedback-note';
        noteContent.innerHTML = feedback.text.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>');
        feedbackContainer.appendChild(noteContent);
    }
    
    // Feedback images
    if (feedback.images && feedback.images.length > 0) {

        const noteHeader = document.createElement('div');
        noteHeader.className = 'section-header';
        noteHeader.innerHTML = '<strong>Images</strong>';
        feedbackContainer.append(noteHeader);
        
        const imagesContainer = document.createElement('div');
        imagesContainer.className = 'images-container';

        feedback.images.forEach(imageData => {
            const imageWrapper = document.createElement('div');
            imageWrapper.className = 'image-wrapper';

            const imgEl = document.createElement('img');
            imgEl.src = imageData.image;
            imgEl.alt = "Feedback Image";
            imgEl.className = "answer-image";

            // Open image in a new tab on double-click
            imgEl.addEventListener('dblclick', () => {
                window.open(imageData.image, '_blank');
            });

            imageWrapper.appendChild(imgEl);
            imagesContainer.appendChild(imageWrapper);
        });

        feedbackContainer.appendChild(imagesContainer);
    }
    
    return feedbackContainer;
}
