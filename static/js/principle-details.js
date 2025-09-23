
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
        let enndpoint = `/api/principles/${principleId}/categories`
        if (customer_id) enndpoint = `/api/principles/${principleId}/categories?customer_id=${customer_id}`
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

    // Process each category
    data.categories.forEach(category => {
        // Create category card
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        
        // Category title only (no status)
        const categoryTitle = document.createElement('h3');
        categoryTitle.className = 'category-title';
        categoryTitle.textContent = category.name;
        categoryCard.appendChild(categoryTitle);
        
        // Render category's own selected options first (if any)
        if (category.options && category.options.length > 0) {
            const categorySelectedOptions = category.options.filter(option => option.is_selected);
            if (categorySelectedOptions.length > 0) {
                const categoryOptionsSection = renderOptionsSection(categorySelectedOptions, 'Category Options');
                categoryCard.appendChild(categoryOptionsSection);
            }
        }
        
        // Render subcategories with their selected options
        if (category.subcategories && category.subcategories.length > 0) {
            category.subcategories.forEach(subcategory => {
                const subcategorySelectedOptions = subcategory.options ? subcategory.options.filter(option => option.is_selected) : [];
                
                // Only render subcategory if it has selected options
                if (subcategorySelectedOptions.length > 0) {
                    const subcategorySection = renderSubcategorySection(subcategory, subcategorySelectedOptions);
                    categoryCard.appendChild(subcategorySection);
                }
            });
        }
        
        // Render category feedback if exists
        if (category.feedback) {
            const feedbackSection = renderFeedbackSection(category.feedback);
            categoryCard.appendChild(feedbackSection);
        }
        
        container.appendChild(categoryCard);
    });
    
    // Show message if no categories were processed
    const processedCategories = container.querySelectorAll('.category-card');
    if (processedCategories.length === 0) {
        const noContentDiv = document.createElement('div');
        noContentDiv.className = 'no-content-message';
        noContentDiv.innerHTML = `
            <div class="empty-state">
                <h3>No Content Available</h3>
                <p>No categories found. Please check back later.</p>
            </div>
        `;
        container.appendChild(noContentDiv);
    }
}

// Helper function to render subcategory section with its selected options
function renderSubcategorySection(subcategory, selectedOptions) {
    const subcategoryContainer = document.createElement('div');
    subcategoryContainer.className = 'subcategory-section';
    
    // Subcategory header
    const subcategoryHeader = document.createElement('div');
    subcategoryHeader.className = 'subcategory-header';
    subcategoryHeader.innerHTML = `<strong>${subcategory.name}</strong>`;
    subcategoryContainer.appendChild(subcategoryHeader);
    
    // Selected options for this subcategory
    const optionsList = document.createElement('div');
    optionsList.className = 'options-list subcategory-options';
    
    selectedOptions.forEach(option => {
        const optionItem = document.createElement('div');
        optionItem.className = 'option-item selected';
        optionItem.innerHTML = `
            <span class="option-indicator">✓</span>
            <span class="option-text">${option.text}</span>
        `;
        optionsList.appendChild(optionItem);
    });
    
    subcategoryContainer.appendChild(optionsList);
    return subcategoryContainer;
}

// Helper function to render options section (for category-level options)
function renderOptionsSection(options, headerText = 'Selected Options') {
    if (options.length === 0) {
        return null;
    }
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-section';
    
    const optionsHeader = document.createElement('div');
    optionsHeader.className = 'section-header';
    optionsHeader.innerHTML = `<strong>${headerText}</strong>`;
    optionsContainer.appendChild(optionsHeader);
    
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
    
    // Feedback note
    if (feedback.note) {
        const noteHeader = document.createElement('div');
        noteHeader.className = 'section-header';
        noteHeader.innerHTML = '<strong>Feedback</strong>';
        feedbackContainer.appendChild(noteHeader);
        
        const noteContent = document.createElement('div');
        noteContent.className = 'feedback-note';
        noteContent.innerHTML = feedback.note.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>');
        feedbackContainer.appendChild(noteContent);
    }
    
    // Feedback images
    if (feedback.images && feedback.images.length > 0) {
        const imagesHeader = document.createElement('div');
        
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