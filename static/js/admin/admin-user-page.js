const pagesContainer = document.getElementById('pages-container');
const getPreviousPageBtn = document.getElementById('pagination-previous-btn');
const getNextPageBtn = document.getElementById('pagination-next-btn');

const users = []
let selectedUserId = null;
let currentPage = 1;
const perPage = 2;
let headers = {
    'X-CSRFToken': getCookie('csrftoken'),
    "Content-Type": 'application/json'
};


const paginationNextBtn = document.getElementById("pagination-next-btn");
const paginationBackBtn = document.getElementById("pagination-back-btn");

async function fetchUsers(page = 1, searchQuery = "") {
    try {
        let url = `/api/admin/user-management?page=${page}&perPage=${perPage}`;
        if(searchQuery){
            url += `&search=${encodeURIComponent(searchQuery)}`; // add search query
        }
        let response = await requestAPI(url, null, headers, "GET");        
        let res = await response.json()
        if (response.status == 200 && res.data) {
            const fetchedUsers = res.data.map(user => ({
                id: user.id ,
                name:user.name || "Not Provided",
                email: user.email || "Not Provided",
                created_at : formatDate(user.created_at),
                
            }));

            currentPage = page; 
            populateTable(fetchedUsers);
            generatePagination(res.pagination.currentPage, res.pagination.total, res.pagination.links.previous, res.pagination.links.next);
        } else {
            console.error("Invalid API response:", response);
        }
    } catch (error) {
        console.error("API request failed:", error);
    }
   
}

const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
searchBtn.addEventListener("click",function(){
    const query = searchInput.value;
    fetchUsers(page = 1,query)
})

function formatDate(isoString) {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');       // e.g., 01
    const month = String(date.getMonth() + 1).padStart(2, '0'); // e.g., 02 (Jan is 0)
    const year = date.getFullYear();                            // e.g., 2025
    return `${day}-${month}-${year}`;
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
            span.addEventListener("click", () => fetchUsers(page));
        }
    });

    if (previousLink) {
        getPreviousPageBtn.setAttribute("onclick", `fetchUsers(${currentPage - 1})`);
        getPreviousPageBtn.classList.remove('opacity-point-3-5');
        getPreviousPageBtn.classList.add('cursor-pointer', 'active');
    } else {
        getPreviousPageBtn.removeAttribute("onclick");
        getPreviousPageBtn.classList.add('opacity-point-3-5');
        getPreviousPageBtn.classList.remove('cursor-pointer', 'active');
    }

    if (nextLink) {
        getNextPageBtn.setAttribute("onclick", `fetchUsers(${currentPage + 1})`);
        getNextPageBtn.classList.remove('opacity-point-3-5');
        getNextPageBtn.classList.add('cursor-pointer', 'active');
    } else {
        getNextPageBtn.removeAttribute("onclick");
        getNextPageBtn.classList.add('opacity-point-3-5');
        getNextPageBtn.classList.remove('cursor-pointer', 'active');
    }
}

function getPage(pageNumber) {
    console.log("Clicked page:", pageNumber);
}

document.addEventListener("DOMContentLoaded", function () {
    const res = {
        pagination: {
            currentPage: 1,
            total: 10,
            links: {
                previous: null,
                next: null
            },
            perPage: 1,
            count: 100
        }
    };
    generatePagination(res.pagination.currentPage, res.pagination.total, res.pagination.links.previous, res.pagination.links.next);
    
    
});

const filterOptions = document.querySelectorAll("#filterOptionList .dropdown-item");
    filterOptions.forEach(option => {
        option.addEventListener("click",function(e){
        e.preventDefault();
        const filterParam = e.target.getAttribute("data-filter");
        console.log(`${filterParam} is being selected`);
        applyFilter(filterParam);
    })
})



// function applyFilter(filterParam) {
//     activeFilter = filterParam;
//     fetchUsers(1);
// }

// function goBack() {
//     if (res.pagination.currentPage > 1) {
//         res.pagination.currentPage--;
//         generatePages(res.pagination.currentPage, res.pagination.total, null, null);
//     }
// }

// function goNext() {
//     if (res.pagination.currentPage < res.pagination.total) {
//         res.pagination.currentPage++;
//         generatePages(res.pagination.currentPage, res.pagination.total, null, null);
//     }
// }


fetchUsers();


const adminUserTableBody = document.getElementById("admin-user-table-body");


function populateTable(fetchedUsers){
    adminUserTableBody.innerHTML = "";
    if (!fetchedUsers || fetchedUsers.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td colspan="4" class="no-user-msg">
        No user has been found.
      </td>
    `;
    adminUserTableBody.appendChild(tr);
    return; // Stop further execution
    }
    fetchedUsers.forEach(user =>{
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <tr>
                <td><span>${user.id}</span></td>
                <td><span>${user.name}</span></td>
                <td><span>${user.email}</span></td>
                <td><span>${user.created_at}</span></td>
            </tr>
        `
        adminUserTableBody.appendChild(tr);

    })

 }