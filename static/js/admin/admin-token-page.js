const pagesContainer = document.getElementById('pages-container');
const getPreviousPageBtn = document.getElementById('pagination-previous-btn');
const getNextPageBtn = document.getElementById('pagination-next-btn');

let tableBody = document.querySelector("#token-container");

let tokensEndpoint = `/api/admin/tokens?perPage=10`;
let tokensData = [];
let deleteId = null;

window.addEventListener('load', getTokens(tokensEndpoint));


async function getTokens(url) {
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(url, null, headers, 'GET');
        response.json().then(function (res) {
            if (response.status == 200) {
                tokensData = [...res.data];
                renderTokens(res.data);
                generatePagination(res.pagination.currentPage, res.pagination.total, res.pagination.links.previous, res.pagination.links.next);
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

function renderTokens(data) {
    tableBody.innerHTML = '';

    if (data.length == 0) {
        tableBody.innerHTML += `
                <tr >
                    <td colspan="6">No data available.</td>
                </tr>`
    } else {
        data.forEach(item => {
            tableBody.innerHTML += `
                <tr>
                    <td>${item?.id || "--"}</td>
                    <td>${item?.email || "--"}</td>
                    <td>${item?.token || "--"}</td>
                    <td>${formatDate(item?.created_at) || "--"}</td>
                    <td>
                        <div class="parent-container-for-status">
                        ${item.is_used
                    ?
                    '<span class="used-status">Used</span>'
                    :
                    '<span class="unused-status">Unused</span>'
                }
                        </div>
                    </td>
                    <td>
                        <div class="action_button">
                            <div>
                                <svg width="33" height="32" viewBox="0 0 33 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0_9538_6684)">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M16.4297 6.5V8.72222C20.7175 8.72222 24.2075 12.2111 24.2075 16.5C24.2075 20.7889 20.7175 24.2778 16.4297 24.2778C12.1419 24.2778 8.65191 20.7889 8.65191 16.5C8.65191 14.4478 9.46857 12.5156 10.8741 11.0756V13.7222H13.0964V7.61111H6.98524V9.83333H8.97524C7.35302 11.6467 6.42969 14.01 6.42969 16.5C6.42969 22.0133 10.9152 26.5 16.4297 26.5C21.9441 26.5 26.4297 22.0133 26.4297 16.5C26.4297 10.9867 21.9441 6.5 16.4297 6.5Z" fill="#71BF1E"/>
                                    </g>
                                    <defs>
                                        <clipPath id="clip0_9538_6684">
                                            <rect width="20" height="20" fill="white" transform="translate(6.42969 6.5)"/>
                                        </clipPath>
                                    </defs>
                                </svg>
                            </div>
                            <div>
                                <svg class="cursor-pointer" onclick="openDeleteModal(${item?.id})" width="33" height="32" viewBox="0 0 33 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M24.7005 12.1913L24.3005 24.2983C24.2664 25.3352 23.8296 26.318 23.0828 27.0381C22.336 27.7583 21.338 28.159 20.3005 28.1553H12.7005C11.6637 28.159 10.6663 27.7588 9.91956 27.0396C9.17285 26.3203 8.73561 25.3385 8.70052 24.3023L8.30052 12.1913C8.29176 11.9261 8.38873 11.6683 8.57007 11.4746C8.75142 11.2808 9.0023 11.1671 9.26752 11.1583C9.53273 11.1496 9.79056 11.2465 9.98429 11.4279C10.178 11.6092 10.2918 11.8601 10.3005 12.1253L10.7005 24.2353C10.7204 24.7523 10.9399 25.2414 11.3128 25.6C11.6858 25.9586 12.1832 26.1587 12.7005 26.1583H20.3005C20.8185 26.1587 21.3165 25.958 21.6895 25.5986C22.0626 25.2392 22.2816 24.749 22.3005 24.2313L22.7005 12.1253C22.7093 11.8601 22.823 11.6092 23.0167 11.4279C23.2105 11.2465 23.4683 11.1496 23.7335 11.1583C23.9987 11.1671 24.2496 11.2808 24.431 11.4746C24.6123 11.6683 24.7093 11.9261 24.7005 12.1913ZM26.0235 8.16232C26.0235 8.42754 25.9182 8.68189 25.7306 8.86943C25.5431 9.05697 25.2887 9.16232 25.0235 9.16232H7.97852C7.7133 9.16232 7.45894 9.05697 7.27141 8.86943C7.08387 8.68189 6.97852 8.42754 6.97852 8.16232C6.97852 7.89711 7.08387 7.64275 7.27141 7.45522C7.45894 7.26768 7.7133 7.16232 7.97852 7.16232H11.0785C11.3954 7.16318 11.7012 7.04611 11.9365 6.83392C12.1718 6.62172 12.3197 6.32957 12.3515 6.01432C12.4253 5.27481 12.7718 4.58925 13.3234 4.09123C13.875 3.59321 14.5923 3.31839 15.3355 3.32032H17.6655C18.4087 3.31839 19.126 3.59321 19.6776 4.09123C20.2293 4.58925 20.5757 5.27481 20.6495 6.01432C20.6813 6.32957 20.8292 6.62172 21.0645 6.83392C21.2998 7.04611 21.6057 7.16318 21.9225 7.16232H25.0225C25.2877 7.16232 25.5421 7.26768 25.7296 7.45522C25.9172 7.64275 26.0225 7.89711 26.0225 8.16232H26.0235ZM14.0875 7.16232H18.9155C18.7841 6.86207 18.6982 6.54391 18.6605 6.21832C18.6357 5.97183 18.5204 5.74331 18.3367 5.57703C18.1531 5.41076 17.9142 5.31857 17.6665 5.31832H15.3365C15.0888 5.31857 14.85 5.41076 14.6663 5.57703C14.4827 5.74331 14.3673 5.97183 14.3425 6.21832C14.3045 6.54396 14.2193 6.86212 14.0875 7.16232ZM15.0945 22.3133V13.7983C15.0945 13.5331 14.9892 13.2788 14.8016 13.0912C14.6141 12.9037 14.3597 12.7983 14.0945 12.7983C13.8293 12.7983 13.5749 12.9037 13.3874 13.0912C13.1999 13.2788 13.0945 13.5331 13.0945 13.7983V22.3173C13.0945 22.5825 13.1999 22.8369 13.3874 23.0244C13.5749 23.212 13.8293 23.3173 14.0945 23.3173C14.3597 23.3173 14.6141 23.212 14.8016 23.0244C14.9892 22.8369 15.0945 22.5825 15.0945 22.3173V22.3133ZM19.9085 22.3133V13.7983C19.9085 13.5331 19.8032 13.2788 19.6156 13.0912C19.4281 12.9037 19.1737 12.7983 18.9085 12.7983C18.6433 12.7983 18.3889 12.9037 18.2014 13.0912C18.0139 13.2788 17.9085 13.5331 17.9085 13.7983V22.3173C17.9085 22.5825 18.0139 22.8369 18.2014 23.0244C18.3889 23.212 18.6433 23.3173 18.9085 23.3173C19.1737 23.3173 19.4281 23.212 19.6156 23.0244C19.8032 22.8369 19.9085 22.5825 19.9085 22.3173V22.3133Z" fill="#F02023"/>
                                </svg>
                            </div>
                        </div>
                    </td>
                </tr>`
        });
    }
}


function generatePagination(currentPage, totalPages, previousLink, nextLink) {
    pagesContainer.innerHTML = '';

    let startPage = Math.max(1, currentPage - 1);
    let endPage = Math.min(totalPages, startPage + 2);

    if (endPage - startPage < 2) {
        startPage = Math.max(1, endPage - 2);
    }

    if (startPage > 1) {
        pagesContainer.innerHTML += `<span class="cursor-pointer">1</span>`;
        if (startPage > 2) {
            pagesContainer.innerHTML += `<span class="ellipsis-container">...</span>`;
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        pagesContainer.innerHTML += `<span${i === currentPage ? ' class="active"' : ' class="cursor-pointer"'}>${i}</span>`;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagesContainer.innerHTML += `<span class="ellipsis-container">...</span>`;
        }
        pagesContainer.innerHTML += `<span class="cursor-pointer">${totalPages}</span>`;
    }

    pagesContainer.querySelectorAll('span').forEach((span) => {
        if ((!span.classList.contains('active')) && (!span.classList.contains('ellipsis-container'))) {
            let page = span.innerText;
            let pageUrl = setParams(tokensEndpoint, 'page', page);
            span.addEventListener("click", () => getTokens(pageUrl));
        }
    });

    if (previousLink) {
        let pageUrl = setParams(tokensEndpoint, 'page', currentPage - 1);
        getPreviousPageBtn.setAttribute("onclick", `getTokens('${pageUrl}')`);
        getPreviousPageBtn.classList.remove('opacity-point-3-5');
        getPreviousPageBtn.classList.add('cursor-pointer', 'active');
    } else {
        getPreviousPageBtn.removeAttribute("onclick");
        getPreviousPageBtn.classList.add('opacity-point-3-5');
        getPreviousPageBtn.classList.remove('cursor-pointer', 'active');
    }

    if (nextLink) {
        let pageUrl = setParams(tokensEndpoint, 'page', currentPage + 1);
        getNextPageBtn.setAttribute("onclick", `getTokens('${pageUrl}')`);
        getNextPageBtn.classList.remove('opacity-point-3-5');
        getNextPageBtn.classList.add('cursor-pointer', 'active');
    } else {
        getNextPageBtn.removeAttribute("onclick");
        getNextPageBtn.classList.add('opacity-point-3-5');
        getNextPageBtn.classList.remove('cursor-pointer', 'active');
    }
}


function searchForm(event) {
    event.preventDefault();
    let form = event.currentTarget;
    let formData = new FormData(form);
    let data = formDataToObject(formData);
    tokensEndpoint = setParams(tokensEndpoint, 'search', `${data.search}`);
    tokensEndpoint = setParams(tokensEndpoint, 'page', '1');
    getTokens(tokensEndpoint);
}


function openDeleteModal(id) {
    deleteId = id;
    let deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    deleteModal.show();
}

document.getElementById('confirmDeleteBtn').addEventListener('click', async function () {
    if (deleteId) {
        await deleteToken(deleteId);
        deleteId = null;
        bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal')).hide();
    }
});


async function deleteToken(id) {
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(`/api/admin/tokens/${id}`, null, headers, 'DELETE');
        if (response.status == 204) {
            showToast("Success", `Token deleted successfully!`, "success-toast");
            getTokens(tokensEndpoint);
        }
        else {
            console.log(res)
            return false;
        }
    }
    catch (err) {
        console.log(err);
    }
}



const modalElement = document.getElementById('generateTokenModal');
const bsModal = new bootstrap.Modal(modalElement);
const generateTokenBtn = document.getElementById('generateTokenBtn');
const tokenDescription = modalElement.querySelector('.token-description');
const tokenLabel = modalElement.querySelector('.token-label');
const spinner = generateTokenBtn.querySelector('.spinner-border');
const btnText = generateTokenBtn.querySelector('.btn-text');
const emailInput = modalElement.querySelector('input[name="email-address"]');
const defaultText = 'Generated token should be display here.';

// Expose function so inline onclick="openGenerateTokenModal()" works
window.openGenerateTokenModal = function () {
    tokenLabel.style.display = 'none';
    tokenDescription.textContent = defaultText;
    tokenDescription.classList.remove('text-success');
    emailInput.value = '';
    bsModal.show();
};

// Reset modal when closed
modalElement.addEventListener('hidden.bs.modal', function () {
    tokenLabel.style.display = 'none';
    tokenDescription.textContent = defaultText;
    tokenDescription.classList.remove('text-success');
    emailInput.value = '';
});

// Generate token on button click
generateTokenBtn.addEventListener('click', async function (e) {
    e.preventDefault();
    const email = emailInput.value.trim();
    if (!email) {
        alert('Please enter a valid email address.');
        return;
    }

    // show spinner + disable button
    spinner.classList.remove('hide');
    btnText.textContent = 'Generating...';
    generateTokenBtn.disabled = true;
    generateTokenBtn.style.opacity = '0.5';
    generateTokenBtn.style.cursor = 'not-allowed';

    try {
        const response = await fetch('/api/admin/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (response.ok && data.data && data.data.token) {
            const token = data.data.token;

            // wait 0.5s for smoother UI transition
            await new Promise(resolve => setTimeout(resolve, 500));

            tokenLabel.style.display = 'none';
            tokenDescription.textContent =
                `The token has been generated successfully against the provided email. Kindly share this token with the user so they can use it to complete the signup process: ${token}`;
            tokenDescription.classList.add('text-success');
            closeCurrentModal();
            getTokens(tokensEndpoint);
        } else {
            tokenDescription.textContent = data.message || 'Failed to generate token.';
            tokenDescription.classList.remove('text-success');
        }
    } catch (err) {
        tokenDescription.textContent = 'An error occurred. Please try again.';
        tokenDescription.classList.remove('text-success');
        console.error(err);
    } finally {
        // hide spinner but keep button disabled for smoother feel
        spinner.classList.add('hide');
        btnText.textContent = 'Continue';

        // optional small delay before keeping it disabled
        await new Promise(resolve => setTimeout(resolve, 500));
    }
});

// Reset modal state every time it closes
modalElement.addEventListener('hidden.bs.modal', function () {
    tokenLabel.style.display = 'none';
    tokenDescription.textContent = 'Generated token should be display here.';
    tokenDescription.classList.remove('text-success');
    emailInput.value = '';

    // reset button state
    generateTokenBtn.disabled = false;
    generateTokenBtn.style.opacity = '1';
    generateTokenBtn.style.cursor = 'pointer';
    spinner.classList.add('hide');
    btnText.textContent = 'Continue';
});