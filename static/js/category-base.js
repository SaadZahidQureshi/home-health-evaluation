let principleId = JSON.parse(document.getElementById("principleId").textContent) || null;
let principle_data = null;
let selectedQuestionsByCategory = new Map();
let questionsWithInitialAnswers = new Set();
let customer_id = sessionStorage.getItem("customer_id") || null;
let notApplicableSelections = new Map();
window.addEventListener('load', get_principle_data());

async function get_principle_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let enndpoint = `${API_BASE_URL}principles/${principleId}/categories`
        if (customer_id) enndpoint = `${API_BASE_URL}principles/${principleId}/categories?customer_id=${customer_id}`
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
        titleDiv.innerHTML = `<h4>${category.name}</h4>`;
        const contentDiv = document.createElement('div');
        contentDiv.className = 'accordian_cnt';
        
        if (category.options && category.options.length > 0) {
            const firstOption = category.applicable ? category.options[0] : {text: 'Not Applicable'};
            
            // contentDiv.innerHTML = `
            //     <p>${firstOption?.text || 'No options available'}</p>
            //     <img src="/static/img/down.svg" alt="">
            // `;
            contentDiv.innerHTML = `
                <p></p>
                <img src="/static/img/down.svg" alt="">
            `;
            
            const innerDiv = document.createElement('div');
            innerDiv.className = 'accordian_inner';
            const ul = document.createElement('ul');
            
            const notApplicableLi = document.createElement('li');
            notApplicableLi.innerHTML = `
                <label class="question-checkbox-label">
                    <input type="checkbox" class="question-checkbox not-applicable-option" 
                           data-question-id="not_applicable_${category.id}" 
                           data-category-id="${category.id}"
                           ${!category.applicable ? 'checked' : ''}>
                    <span class="question-text">Not Applicable</span>
                </label>
            `;
            ul.appendChild(notApplicableLi);
            
            category.options.forEach(option => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <label class="question-checkbox-label">
                        <input type="checkbox" class="question-checkbox" 
                               data-question-id="${option.id}" 
                               data-category-id="${category.id}"
                               ${option.is_selected ? 'checked' : ''}
                               ${!category.applicable ? 'disabled' : ''}>
                        <span class="question-text">${option.text}</span>
                    </label>
                `;
                ul.appendChild(li);
            });
            
            innerDiv.appendChild(ul);
            
            const formContainer = document.createElement('div');
            formContainer.className = 'form-container';
            formContainer.style.display = 'block';
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(contentDiv);
            accordionBox.appendChild(innerDiv);
            accordionBox.appendChild(formContainer);
            container.appendChild(accordionBox);
            
            const categoryId = category.id;
            if (!selectedQuestionsByCategory.has(categoryId)) {
                selectedQuestionsByCategory.set(categoryId, new Set());
            }
            
            if (!category.applicable) {
                notApplicableSelections.set(categoryId, true);
            }
            
            if (!category.applicable) {
                category.options.forEach(option => {
                    if (option.is_selected) {
                        selectedQuestionsByCategory.get(categoryId).add(option.id.toString());
                    }
                });
            }
            
            renderQuestionForm(formContainer, Array.from(selectedQuestionsByCategory.get(categoryId)), data, contentDiv.querySelector('p'), categoryId);
            
        } else if (category.subcategories && category.subcategories.length > 0) {
            const firstSubcategory = category.subcategories[0];
            let firstOptionText = '';
            
            const findFirstOption = (subcat) => {
                if (!subcat.applicable) {
                    return 'Not Applicable';
                }
                if (subcat.options && subcat.options.length > 0) {
                    return subcat.options[0].text;
                }
                if (subcat.subcategories && subcat.subcategories.length > 0) {
                    return findFirstOption(subcat.subcategories[0]);
                }
                return 'No options available';
            };
            
            firstOptionText = findFirstOption(firstSubcategory);
            
            contentDiv.innerHTML = `
                <p><img src="/static/img/right.svg" alt=""></p>
                <img src="/static/img/down.svg" alt="">
            `;
            
            const innerDiv = document.createElement('div');
            innerDiv.className = 'accordian_inner pest_inner';
            const ul = document.createElement('ul');
            
            const renderSubcategories = (subcategories, parentUl) => {
                subcategories.forEach(subcat => {
                    const li = document.createElement('li');
                    
                    if (subcat.subcategories && subcat.subcategories.length > 0) {
                        li.innerHTML = `
                            <a href="#" class="question-link pest-type-link" data-subcat-id="${subcat.id}">
                                ${subcat.name} 
                                <img src="/static/img/arrow-right.svg" alt="">
                            </a>
                        `;
                        
                        const subUl = document.createElement('ul');
                        subUl.className = 'pest_dropdown';
                        subUl.style.display = 'none';
                        
                        const subcatNotApplicableLi = document.createElement('li');
                        subcatNotApplicableLi.innerHTML = `
                            <label class="question-checkbox-label">
                                <input type="checkbox" class="question-checkbox not-applicable-option subcategory-na" 
                                       data-question-id="not_applicable_${subcat.id}" 
                                       data-subcategory-id="${subcat.id}"
                                       data-main-category-id="${category.id}"
                                       ${!subcat.applicable ? 'checked' : ''}
                                       ${!category.applicable ? 'disabled' : ''}>
                                <span class="question-text">Not Applicable</span>
                            </label>
                        `;
                        subUl.appendChild(subcatNotApplicableLi);
                        
                        renderSubcategories(subcat.subcategories, subUl);
                        li.appendChild(subUl);
                        
                    } else if (subcat.options && subcat.options.length > 0) {
                        li.innerHTML = `
                            <a href="#" class="question-link pest-type-link" data-subcat-id="${subcat.id}">
                                ${subcat.name} 
                                <img src="/static/img/arrow-right.svg" alt="">
                            </a>
                        `;
                        
                        const optionsUl = document.createElement('ul');
                        optionsUl.className = 'pest_dropdown';
                        optionsUl.style.display = 'none';
                        
                        const subcatNotApplicableLi = document.createElement('li');
                        subcatNotApplicableLi.innerHTML = `
                            <label class="question-checkbox-label">
                                <input type="checkbox" class="question-checkbox not-applicable-option subcategory-na" 
                                       data-question-id="not_applicable_${subcat.id}" 
                                       data-subcategory-id="${subcat.id}"
                                       data-main-category-id="${category.id}"
                                       ${!subcat.applicable ? 'checked' : ''}
                                       ${!category.applicable ? 'disabled' : ''}>
                                <span class="question-text">Not Applicable</span>
                            </label>
                        `;
                        optionsUl.appendChild(subcatNotApplicableLi);
                        
                        subcat.options.forEach(option => {
                            const optionLi = document.createElement('li');
                            optionLi.innerHTML = `
                                <label class="question-checkbox-label">
                                    <input type="checkbox" class="question-checkbox" 
                                           data-question-id="${option.id}" 
                                           data-subcategory-id="${subcat.id}"
                                           data-main-category-id="${category.id}"
                                           ${option.is_selected ? 'checked' : ''}
                                           ${!subcat.applicable || !category.applicable ? 'disabled' : ''}>
                                    <span class="question-text">${option.text}</span>
                                </label>
                            `;
                            optionsUl.appendChild(optionLi);
                        });
                        
                        li.appendChild(optionsUl);
                    } else {
                        li.innerHTML = `
                            <div class="empty-subcategory">
                                <span>No options available</span>
                            </div>
                        `;
                    }
                    
                    parentUl.appendChild(li);
                });
            };
            
            renderSubcategories(category.subcategories, ul);
            innerDiv.appendChild(ul);
            
            const formContainer = document.createElement('div');
            formContainer.className = 'form-container';
            formContainer.style.display = 'block';
            
            accordionBox.appendChild(titleDiv);
            accordionBox.appendChild(contentDiv);
            accordionBox.appendChild(innerDiv);
            accordionBox.appendChild(formContainer);
            container.appendChild(accordionBox);
            
            const categoryId = category.id;
            if (!selectedQuestionsByCategory.has(categoryId)) {
                selectedQuestionsByCategory.set(categoryId, new Set());
            }
            
            if (!category.applicable) {
                notApplicableSelections.set(categoryId, true);
            }
            
            const initializeSubcategories = (subcategories) => {
                subcategories.forEach(subcat => {
                    if (!selectedQuestionsByCategory.has(subcat.id)) {
                        selectedQuestionsByCategory.set(subcat.id, new Set());
                    }
                    
                    if (!subcat.applicable) {
                        notApplicableSelections.set(subcat.id, true);
                    }
                    
                    if (subcat.options && !subcat.applicable && !category.applicable) {
                        subcat.options.forEach(option => {
                            if (option.is_selected) {
                                selectedQuestionsByCategory.get(subcat.id).add(option.id.toString());
                            }
                        });
                    }
                    if (subcat.subcategories) {
                        initializeSubcategories(subcat.subcategories);
                    }
                });
            };
            
            initializeSubcategories(category.subcategories);
            
            const pestTypeLinks = accordionBox.querySelectorAll('.pest-type-link');
            pestTypeLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const subcatId = this.getAttribute('data-subcat-id');
                    
                    const allDropdowns = accordionBox.querySelectorAll('.pest_dropdown');
                    allDropdowns.forEach(dropdown => {
                        dropdown.style.display = 'none';
                    });
                    
                    const targetDropdown = this.nextElementSibling;
                    if (targetDropdown && targetDropdown.classList.contains('pest_dropdown')) {
                        targetDropdown.style.display = 'block';
                    }
                    
                    const findSubcategoryPath = (subcategories, targetId) => {
                        for (const subcat of subcategories) {
                            if (!subcat.applicable)
                                return { name: subcat.name, firstOption: 'Not Applicable' }
                            if (subcat.id.toString() === targetId) {
                                return {
                                    name: subcat.name,
                                    firstOption: subcat.options?.[0]?.text || 'No options available'
                                };
                            }
                            if (subcat.subcategories) {
                                const found = findSubcategoryPath(subcat.subcategories, targetId);
                                if (found) {
                                    return {
                                        name: `${subcat.name} > ${found.name}`,
                                        firstOption: found.firstOption
                                    };
                                }
                            }
                        }
                        return null;
                    };
                    
                    const pathInfo = findSubcategoryPath(category.subcategories, subcatId);
                    if (pathInfo) {
                        contentDiv.innerHTML = `
                            <p>${pathInfo.name} <img src="/static/img/right.svg" alt=""> ${pathInfo.firstOption}</p>
                            <img src="/static/img/down.svg" alt="">
                        `;
                    }
                });
            });
            
            renderQuestionForm(formContainer, [], data, contentDiv.querySelector('p'), categoryId);
            
        } else {
            contentDiv.innerHTML = `
                <p>No options available</p>
                <img src="/static/img/down.svg" alt="">
            `;
            
            const innerDiv = document.createElement('div');
            innerDiv.className = 'accordian_inner empty-category';
            innerDiv.innerHTML = `
                <div class="empty-category-message">
                    <span>No options available for this category</span>
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
            
            renderQuestionForm(formContainer, [], data, contentDiv.querySelector('p'), category.id);
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

function setupEventHandlers(data) {
    $(".accordian_cnt").click(function() {
        $(this).toggleClass("active").next().slideToggle();
    });
    
    questionsWithInitialAnswers.clear();
    
    const collectInitialAnswers = (categories) => {
        categories.forEach(category => {
            if (category.options) {
                category.options.forEach(option => {
                    if (option.is_selected) {
                        questionsWithInitialAnswers.add(option.id.toString());
                    }
                });
            }
            if (category.subcategories) {
                collectInitialAnswers(category.subcategories);
            }
        });
    };
    
    const initializeSelections = (categories) => {
        categories.forEach(category => {
            if (!selectedQuestionsByCategory.has(category.id)) {
                selectedQuestionsByCategory.set(category.id, new Set());
            }
            
            if (category.options) {
                category.options.forEach(option => {
                    if (option.is_selected) {
                        selectedQuestionsByCategory.get(category.id).add(option.id.toString());
                    }
                });
            }
            
            if (category.subcategories) {
                initializeSelections(category.subcategories);
            }
        });
    };
    
    initializeSelections(data.categories);
    collectInitialAnswers(data.categories);
    
    data.categories.forEach(category => {
        const accordionBox = document.querySelector(`[data-category-id="${category.id}"]`)?.closest('.accordian_box');
        if (!accordionBox) return;
        
        const formContainer = accordionBox.querySelector('.form-container');
        const contentDiv = accordionBox.querySelector('.accordian_cnt');
        const contentP = contentDiv.querySelector('p');
        
        const currentSelections = selectedQuestionsByCategory.get(category.id) || new Set();
        renderQuestionForm(formContainer, Array.from(currentSelections), data, contentP, category.id);
        
        updateAccordionContentCount(category, contentP);
    });
    
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('question-checkbox')) {
            const questionId = e.target.getAttribute('data-question-id');
            const accordionBox = e.target.closest('.accordian_box');
            const formContainer = accordionBox.querySelector('.form-container');
            const contentDiv = accordionBox.querySelector('.accordian_cnt');
            const contentP = contentDiv.querySelector('p');
            
            // formContainer.style.display = 'block';
            
            
            if (e.target.classList.contains('not-applicable-option')) {
                if (e.target.classList.contains('main-category-na')) {
                    handleMainCategoryNotApplicable(e.target, accordionBox, data);
                } else if (e.target.classList.contains('subcategory-na')) {
                    handleSubcategoryNotApplicable(e.target, accordionBox, data);
                } else {
                    handleRegularCategoryNotApplicable(e.target, accordionBox, data);
                }
                
                const categoryId = e.target.getAttribute('data-category-id') || 
                                 e.target.getAttribute('data-main-category-id');
                if (categoryId) {
                    const category = findCategoryById(data.categories, parseInt(categoryId));
                    if (category) {
                        updateAccordionContentCount(category, contentP);
                    }
                }
                // Add this logic after the handlers:
                // const categoryId = e.target.getAttribute('data-category-id') || 
                //                 e.target.getAttribute('data-main-category-id');
                if (categoryId) {
                    const category = findCategoryById(data.categories, parseInt(categoryId));
                    if (category) {
                        // Check if form should be hidden
                        let shouldHideForm = false;
                        
                        if (category.subcategories && category.subcategories.length > 0) {
                            const allSubcategoriesNotApplicable = category.subcategories.every(subcat => 
                                notApplicableSelections.has(subcat.id) || checkAllNestedSubcategoriesNotApplicable(subcat)
                            );
                            shouldHideForm = allSubcategoriesNotApplicable;
                        } else {
                            shouldHideForm = notApplicableSelections.has(category.id);
                        }
                        
                        formContainer.style.display = shouldHideForm ? 'none' : 'block';
                        updateAccordionContentCount(category, contentP);
                    }
                }
                return;
            }
            
            const subcategoryId = e.target.getAttribute('data-subcategory-id');
            const mainCategoryId = e.target.getAttribute('data-main-category-id') || e.target.getAttribute('data-category-id');
            
            if (e.target.checked) {
                const currentContainer = e.target.closest('ul') || accordionBox;
                const notApplicableOptions = currentContainer.querySelectorAll('.not-applicable-option');
                
                notApplicableOptions.forEach(naOption => {
                    if (naOption.checked) {
                        naOption.checked = false;
                        const naCategoryId = naOption.getAttribute('data-category-id') || naOption.getAttribute('data-subcategory-id');
                        if (naCategoryId) {
                            notApplicableSelections.delete(parseInt(naCategoryId));
                        }
                    }
                });
                
                const currentCategoryId = mainCategoryId || subcategoryId;
                const currentSelections = selectedQuestionsByCategory.get(parseInt(currentCategoryId)) || new Set();
                renderQuestionForm(formContainer, Array.from(currentSelections), data, contentP, mainCategoryId);
            }
            
            if (subcategoryId) {
                handleSubcategoryOptionChange(e.target, subcategoryId, questionId, e.target.checked);
            } else if (mainCategoryId) {
                handleMainCategoryOptionChange(e.target, mainCategoryId, questionId, e.target.checked, questionsWithInitialAnswers);
            }
            
            const categoryId = mainCategoryId || subcategoryId;
            if (categoryId) {
                const category = findCategoryById(data.categories, parseInt(categoryId));
                if (category) {
                    updateAccordionContentCount(category, contentP);
                }
            }
            
            if (!contentDiv.classList.contains('active')) {
                contentDiv.click();
            }
        }
    });
}

function findCategoryById(categories, categoryId) {
    for (const category of categories) {
        if (category.id === categoryId) {
            return category;
        }
        if (category.subcategories) {
            const found = findCategoryById(category.subcategories, categoryId);
            if (found) return found;
        }
    }
    return null;
}

function countSelectedOptions(category) {
    let count = 0;
    
    const categorySelections = selectedQuestionsByCategory.get(category.id);
    if (categorySelections) {
        count += categorySelections.size;
    }
    
    if (category.subcategories) {
        category.subcategories.forEach(subcat => {
            count += countSelectedOptions(subcat);
        });
    }
    
    return count;
}

function updateAccordionContentCount(category, contentP) {
    if (!contentP) return;
    
    const selectedCount = countSelectedOptions(category);
    let currentContent = contentP.innerHTML;
    
    let baseContent = currentContent;
    baseContent = baseContent.replace(/\d+\s+option[s]?\s+selected\s*/i, '');
    baseContent = baseContent.replace(/Select options\s*/i, '');
    
    const imgMatch = baseContent.match(/(<img[^>]*>)/i);
    const imgTag = imgMatch ? imgMatch[0] : '<img src="/static/img/down.svg" alt="">';
    
    baseContent = baseContent.replace(/<img[^>]*>/i, '').trim();
    
    if (selectedCount > 0) {
        const countText = `${selectedCount} option${selectedCount > 1 ? 's' : ''} selected`;
        contentP.innerHTML = `${baseContent} ${countText}`;
    } else {
        contentP.innerHTML = `${baseContent} Select options `;
    }
}

function handleMainCategoryNotApplicable(checkbox, accordionBox, data) {
    const categoryId = parseInt(checkbox.getAttribute('data-category-id'));
    const formContainer = accordionBox.querySelector('.form-container');
    
    if (checkbox.checked) {
        notApplicableSelections.set(categoryId, true);
        
        const allCheckboxes = accordionBox.querySelectorAll('.question-checkbox:not(.main-category-na)');
        allCheckboxes.forEach(cb => {
            cb.checked = false;
            cb.disabled = true;
            
            const qId = cb.getAttribute('data-question-id');
            const subcatId = cb.getAttribute('data-subcategory-id');
            const mainCatId = cb.getAttribute('data-main-category-id') || cb.getAttribute('data-category-id');
            
            if (subcatId) {
                handleSubcategoryOptionChange(cb, subcatId, qId, false);
            } else if (mainCatId) {
                handleMainCategoryOptionChange(cb, mainCatId, qId, false, questionsWithInitialAnswers);
            }
        });
        
        clearAllCategorySelections(data.categories, categoryId);
        formContainer.style.display = 'block';
        
    } else {
        notApplicableSelections.delete(categoryId);
        
        const allCheckboxes = accordionBox.querySelectorAll('.question-checkbox:not(.main-category-na)');
        allCheckboxes.forEach(cb => {
            cb.disabled = false;
        });
        
        formContainer.style.display = 'block';
    }
}

function handleSubcategoryNotApplicable(checkbox, accordionBox, data) {
    const subcategoryId = parseInt(checkbox.getAttribute('data-subcategory-id'));
    const mainCategoryId = parseInt(checkbox.getAttribute('data-main-category-id'));
    const formContainer = accordionBox.querySelector('.form-container');
    
    if (checkbox.checked) {
        notApplicableSelections.set(subcategoryId, true);
        
        const subcategoryOptions = accordionBox.querySelectorAll(`[data-subcategory-id="${subcategoryId}"]:not(.subcategory-na)`);
        subcategoryOptions.forEach(cb => {
            cb.checked = false;
            cb.disabled = true;
            
            const qId = cb.getAttribute('data-question-id');
            handleSubcategoryOptionChange(cb, subcategoryId, qId, false);
        });
        
        selectedQuestionsByCategory.set(subcategoryId, new Set());
        formContainer.style.display = 'block';
        
    } else {
        notApplicableSelections.delete(subcategoryId);
        
        const subcategoryOptions = accordionBox.querySelectorAll(`[data-subcategory-id="${subcategoryId}"]:not(.subcategory-na)`);
        subcategoryOptions.forEach(cb => {
            cb.disabled = false;
        });
        
        formContainer.style.display = 'block';
    }
}

function handleRegularCategoryNotApplicable(checkbox, accordionBox, data) {
    const categoryId = parseInt(checkbox.getAttribute('data-category-id'));
    const formContainer = accordionBox.querySelector('.form-container');
    
    if (checkbox.checked) {
        notApplicableSelections.set(categoryId, true);
        
        const allCheckboxes = accordionBox.querySelectorAll('.question-checkbox:not(.not-applicable-option)');
        allCheckboxes.forEach(cb => {
            cb.checked = false;
            cb.disabled = true;
            const qId = cb.getAttribute('data-question-id');
            const catId = cb.getAttribute('data-category-id');
            handleMainCategoryOptionChange(cb, catId, qId, false, questionsWithInitialAnswers);
        });
        
        selectedQuestionsByCategory.set(categoryId, new Set());
        formContainer.style.display = 'block';
        
    } else {
        notApplicableSelections.delete(categoryId);
        
        const allCheckboxes = accordionBox.querySelectorAll('.question-checkbox:not(.not-applicable-option)');
        allCheckboxes.forEach(cb => {
            cb.disabled = false;
        });
        
        formContainer.style.display = 'block';
    }
}

function handleMainCategoryOptionChange(checkbox, categoryId, questionId, isChecked, questionsWithInitialAnswers) {
    if (!selectedQuestionsByCategory.has(parseInt(categoryId))) {
        selectedQuestionsByCategory.set(parseInt(categoryId), new Set());
    }
    
    const categorySelections = selectedQuestionsByCategory.get(parseInt(categoryId));
    
    if (isChecked) {
        categorySelections.add(questionId);
    } else {
        categorySelections.delete(questionId);
        
        if (questionsWithInitialAnswers.has(questionId)) {
            if (!window.questionsToDelete) {
                window.questionsToDelete = new Set();
            }
            window.questionsToDelete.add(questionId);
        }
    }
}

function handleSubcategoryOptionChange(checkbox, subcategoryId, questionId, isChecked) {
    if (!selectedQuestionsByCategory.has(parseInt(subcategoryId))) {
        selectedQuestionsByCategory.set(parseInt(subcategoryId), new Set());
    }
    
    const subcategorySelections = selectedQuestionsByCategory.get(parseInt(subcategoryId));
    
    if (isChecked) {
        subcategorySelections.add(questionId);
    } else {
        subcategorySelections.delete(questionId);
        
        if (questionsWithInitialAnswers.has(questionId)) {
            if (!window.questionsToDelete) {
                window.questionsToDelete = new Set();
            }
            window.questionsToDelete.add(questionId);
        }
    }
}

function clearAllCategorySelections(categories, mainCategoryId) {
    categories.forEach(category => {
        if (category.id === mainCategoryId) {
            selectedQuestionsByCategory.set(category.id, new Set());
            
            if (category.subcategories) {
                const clearSubcategory = (subcategories) => {
                    subcategories.forEach(subcat => {
                        selectedQuestionsByCategory.set(subcat.id, new Set());
                        notApplicableSelections.set(subcat.id, true);
                        if (subcat.subcategories) {
                            clearSubcategory(subcat.subcategories);
                        }
                    });
                };
                clearSubcategory(category.subcategories);
            }
        }
    });
}

function renderQuestionForm(container, questionIds, data, selectedQs, categoryId) {
    let answerData = null;
    const mainCategory = data.categories.find(cat => cat.id === categoryId);
    if (mainCategory && mainCategory.feedback) {
        answerData = {
            details: mainCategory.feedback.note,
            images: mainCategory.feedback.images
        };
    }

    let formHTML = `
        <div class="accordion_selected">
            <div class="template_title">
                <h4>Provide feedback for this category</h4>
            </div>
            <form class="details-form" data-category-id="${categoryId}">
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
                                    <input type="file" name="images" multiple class="image-upload" accept="image/jpeg, image/jpg, image/png"/>
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

async function handleGlobalSubmit(event) {
    event.preventDefault();
    const button = event.target.closest("button");
    const buttonTextEl = button.querySelector(".btn-text");
    const originalButtonText = buttonTextEl ? buttonTextEl.textContent : button.textContent;

    beforeLoad(button);

    try {
        if (window.feedbacksToDelete && window.feedbacksToDelete.size > 0) {
            for (const categoryId of window.feedbacksToDelete) {
                const category = principle_data.categories.find(cat => cat.id === categoryId);
                if (category && category.feedback && category.feedback.id) {
                    await deleteFeedback(category.feedback.id);
                }
            }
            window.feedbacksToDelete.clear();
        }

        for (const category of principle_data.categories) {
            const categoryId = category.id;
            const accordionBox = [...document.querySelectorAll('.accordian_box')]
                .find(box => box.querySelector('.accordian_title h4').textContent === category.name);

            if (!accordionBox) continue;

            const mainCategoryNotApplicable = notApplicableSelections.has(categoryId);

            if (category.subcategories && category.subcategories.length > 0) {
                const saveSubcategorySelections = async (subcategories) => {
                    for (const subcat of subcategories) {
                        const subcatSelections = selectedQuestionsByCategory.get(subcat.id) || new Set();
                        const selectionsToSave = notApplicableSelections.has(subcat.id) ? [] : Array.from(subcatSelections);
                        
                        const selectionSuccess = await saveCategorySelections(subcat.id, selectionsToSave);
                        if (!selectionSuccess) {
                            throw new Error(`Failed to save selections for subcategory in "${category.name}"`);
                        }
                        
                        if (subcat.subcategories) {
                            await saveSubcategorySelections(subcat.subcategories);
                        }
                    }
                };
                
                await saveSubcategorySelections(category.subcategories);
            } else {
                const categorySelections = selectedQuestionsByCategory.get(categoryId) || new Set();
                const selectionsToSave = mainCategoryNotApplicable ? [] : Array.from(categorySelections);
                
                const selectionSuccess = await saveCategorySelections(categoryId, selectionsToSave);
                if (!selectionSuccess) {
                    throw new Error(`Failed to save selections for "${category.name}"`);
                }
            }

            if (!mainCategoryNotApplicable) {
                const form = accordionBox.querySelector('.details-form');
                
                let shouldSaveFeedback = false;
                let hasAnySelections = false;

                if (category.subcategories && category.subcategories.length > 0) {
                    const allSubcategoriesNotApplicable = category.subcategories.every(subcat => 
                        notApplicableSelections.has(subcat.id) || checkAllNestedSubcategoriesNotApplicable(subcat)
                    );

                    if (!allSubcategoriesNotApplicable) {
                        const checkForSelections = (subcategories) => {
                            for (const subcat of subcategories) {
                                if (!notApplicableSelections.has(subcat.id)) {
                                    const subcatSelections = selectedQuestionsByCategory.get(subcat.id) || new Set();
                                    if (subcatSelections.size > 0) {
                                        return true;
                                    }
                                }
                                if (subcat.subcategories && checkForSelections(subcat.subcategories)) {
                                    return true;
                                }
                            }
                            return false;
                        };
                        
                        hasAnySelections = checkForSelections(category.subcategories);
                        shouldSaveFeedback = hasAnySelections;
                    }
                } else {
                    const categorySelections = selectedQuestionsByCategory.get(categoryId) || new Set();
                    hasAnySelections = categorySelections.size > 0;
                    shouldSaveFeedback = hasAnySelections;
                }
                if (shouldSaveFeedback && form) {
                    const formData = new FormData(form);
                    const details = formData.get('details');
                    const imageFiles = formData.getAll('images').filter(file => file.size > 0);
                    const existingImages = [...form.querySelectorAll('.added_item[data-image-id]')]
                        .map(item => item.getAttribute('data-image-id'));

                    if (details.trim() !== '' || imageFiles.length > 0){
                        const feedbackSuccess = await saveMainCategoryFeedback(categoryId, details, imageFiles, existingImages);
                        if (!feedbackSuccess) {
                            throw new Error(`Failed to save feedback for "${category.name}"`);
                        }
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
    } catch (error) {
        console.error("Error in global submit:", error);
        afterLoad(button, originalButtonText);
        button.disabled = false;
        showToast("Error!", error.message || "Something went wrong while saving. Please try again.", "danger-toast");
    }
}

function checkAllNestedSubcategoriesNotApplicable(subcategory) {
    if (subcategory.subcategories && subcategory.subcategories.length > 0) {
        return subcategory.subcategories.every(subcat => 
            notApplicableSelections.has(subcat.id) || checkAllNestedSubcategoriesNotApplicable(subcat)
        );
    }
    return notApplicableSelections.has(subcategory.id);
}

async function saveMainCategoryFeedback(categoryId, details, imageFiles, existingImages) {
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
            `${API_BASE_URL}categories/${categoryId}/feedback`,
            JSON.stringify({
                customer_id: customer_id,
                note: details
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
            const imageResponse = await requestAPI(
                `${API_BASE_URL}categories/${categoryId}/upload-images`,
                imageFormData,
                imageHeaders,
                'POST'
            );

            if (!imageResponse.ok) {
                console.error(`Failed to upload images for category ${categoryId}`);
                return false;
            }
        }

        return true;
    } catch (err) {
        console.error(`Error saving feedback for category ${categoryId}:`, err);
        return false;
    }
}

async function saveCategorySelections(categoryId, selectedOptionIds) {
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
        console.log(selectedOptionIds)

        if (selectedOptionIds.length === 0) {
            return await setNotApplicable(categoryId)
        }
        let data = {
            customer_id: customer_id,
            selected_options: selectedOptionIds
        }
        const selectionResponse = await requestAPI(`${API_BASE_URL}categories/${categoryId}/selection`, JSON.stringify(data), headers, 'POST');
        if (selectionResponse.status !== 200) {
            console.error(`Failed to save selections for category ${categoryId}`);
            return false;
        }
        return true;
    } catch (err) {
        console.error(`Error saving selections for category ${categoryId}:`, err);
        return false;
    }
}

async function setNotApplicable(categoryId) {
    try {
        const headers = { 
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        };
        let data = {customer_id: customer_id}
        const selectionResponse = await requestAPI(`${API_BASE_URL}categories/${categoryId}/applicable`, JSON.stringify(data), headers, 'POST');
        if (selectionResponse.status !== 200) {
            console.error(`Failed to update the category ${categoryId}`);
            return false;
        }
        return true;
    } catch (err) {
        console.error(`Error updating the category ${categoryId}:`, err);
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

function isLastStep() {
    const menuItems = [...document.querySelectorAll('.side_menu ul li')];
    const activeIndex = menuItems.findIndex(li => li.classList.contains('active'));
    return activeIndex === menuItems.length - 1;
}

async function checkAllPrinciplesCompleted() {
    try {
        await get_principle_status_data();
        const allCompleted = principle_status_data.every(item => item.status === 'completed');
        return allCompleted;
    } catch (err) {
        console.error('Error checking principle status:', err);
        return false;
    }
}

async function getCustomerDetails(customerId) {
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`${API_BASE_URL}customers/${customerId}`, null, headers, 'GET');
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
        let response = await requestAPI(`${API_BASE_URL}customers/${customer_id}`, formData, headers, 'PATCH');
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

// Helper functions (keep these as they were)
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

async function createCustomer() {
    try {
        const headers = {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        };
        
        const userResponse = await requestAPI(`${API_BASE_URL}me`, null, headers, 'GET');
        if (!userResponse.ok) {
            throw new Error("Failed to get current user info");
        }
        
        const userData = await userResponse.json();
        const createdById = userData.id;

        const response = await requestAPI(
            `${API_BASE_URL}customers`,
            JSON.stringify({}),
            headers,
            'POST'
        );

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
