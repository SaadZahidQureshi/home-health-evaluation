
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
        let enndpoint = `${API_BASE_URL}principles/${principleId}/categories/questions`
        if (customer_id) enndpoint = `${API_BASE_URL}principles/${principleId}/categories/questions?customer_id=${customer_id}`
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

    // Create principle header
    // const principleHeader = document.createElement('div');
    // principleHeader.className = 'principle-header';
    // principleHeader.innerHTML = `<h2>${data.principle.name}</h2>`;
    // container.appendChild(principleHeader);
    
    // Process each category
    data.categories.forEach(category => {
        // Check if category has any pest types or questions
        if (!category.pest_types || category.pest_types.length === 0) {
            return;
        }
        
        // Check if there are any questions at all in this category
        const hasAnyQuestions = category.pest_types.some(pt => pt.questions && pt.questions.length > 0);
        if (!hasAnyQuestions) {
            return;
        }
        
        // Collect all questions with answers and images from this category
        const questionsWithAnswers = [];
        category.pest_types.forEach(pestType => {
            if (pestType.questions) {
                pestType.questions.forEach(questionData => {
                    if (questionData.answer && 
                        questionData.answer.images && 
                        questionData.answer.images.length > 0) {
                        questionsWithAnswers.push({
                            question: questionData.question,
                            answer: questionData.answer,
                            pestType: pestType.pest_type
                        });
                    }
                });
            }
        });
        
        // Only create category section if it has questions with answers and images
        if (questionsWithAnswers.length === 0) {
            return;
        }
        
        // Create category card
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        
        // Category title
        const categoryTitle = document.createElement('h3');
        categoryTitle.className = 'category-title';
        categoryTitle.textContent = category.category.name;
        categoryCard.appendChild(categoryTitle);
        
        // Process each question with answer in this category
        questionsWithAnswers.forEach((questionData, index) => {
            // Question container
            const questionContainer = document.createElement('div');
            questionContainer.className = 'question-container';
            
            // Question text
            const questionText = document.createElement('div');
            questionText.className = 'question-text';
            questionText.textContent = questionData.question.text;
            questionContainer.appendChild(questionText);
            
            // Comment section
            const commentSection = document.createElement('div');
            commentSection.className = 'comment-section';
            commentSection.innerHTML = `
                <strong>Comment</strong><br>
                ${questionData.answer.details.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')}
            `;
            questionContainer.appendChild(commentSection);
            
            // Images section
            const imagesHeader = document.createElement('div');
            imagesHeader.className = 'images-header';
            imagesHeader.innerHTML = '<strong>Images</strong>';
            questionContainer.appendChild(imagesHeader);
            
            const imagesContainer = document.createElement('div');
            imagesContainer.className = 'images-container';
            
            // Add images for this specific question
            questionData.answer.images.forEach(imageData => {
                const imageWrapper = document.createElement('div');
                imageWrapper.className = 'image-wrapper';
                imageWrapper.innerHTML = `
                    <img src="${imageData.image}" alt="Answer Image" class="answer-image">
                `;
                imagesContainer.appendChild(imageWrapper);
            });
            
            questionContainer.appendChild(imagesContainer);
            categoryCard.appendChild(questionContainer);
        });
        
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
                <p>No answered questions with images found. Please check back later.</p>
            </div>
        `;
        container.appendChild(noContentDiv);
    }
}