console.log("here");

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
        let url = `${API_BASE_URL}admin/user-management?page=${page}&perPage=${perPage}`;
        if(searchQuery){
            url += `&search=${encodeURIComponent(searchQuery)}`; // add search query
        }
        let response = await requestAPI(url, null, headers, "GET");        
        let res = await response.json()
        if (response.status == 200 && res.data) {
            console.log(res.data)
            const fetchedUsers = res.data.map(user => ({
                id: user.id ,
                name:user.name || "Not Provided",
                email: user.email || "Not Provided",
                created_at : formatDate(user.created_at),
                
            }));

            currentPage = page; 
            populateTable(fetchedUsers);
            generatePages(res.pagination.currentPage, res.pagination.total, res.pagination.links.previous, res.pagination.links.next);
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



function generatePages(currentPage, totalPages, previousLink, nextLink) {
    const paginationContainer = document.querySelector(".pagination-container")
    const pagesContainer = document.getElementById('pages-container');
    
    // Hide pagination if only one page
    if (totalPages <= 1) {
      paginationContainer.style.display = 'none';
      return;
    } else {
      paginationContainer.style.display = 'flex'; // or 'block' based on your layout
    }
    pagesContainer.innerHTML = '';

    let startPage = Math.max(1, currentPage - 1);
    let endPage = Math.min(totalPages, startPage + 2);

    if (endPage - startPage < 2) {
        startPage = Math.max(1, endPage - 2);
    }

    if (startPage > 1) {
        pagesContainer.innerHTML += '<span class="cursor-pointer">1</span>';
        if (startPage > 2) {
            pagesContainer.innerHTML += '<span class="ellipsis-container">...</span>';
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        pagesContainer.innerHTML += `<span${i === currentPage ? ' class="active"' : ' class="cursor-pointer"'}>${i}</span>`;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagesContainer.innerHTML += '<span class="ellipsis-container">...</span>';
        }
        pagesContainer.innerHTML += `<span class="cursor-pointer">${totalPages}</span>`;
    }
    pagesContainer.querySelectorAll('span').forEach((span) => {
        if ((!span.classList.contains('active'))  && (!span.classList.contains('ellipsis-container'))) {
            let page = span.innerText;
            span.addEventListener("click", () => fetchUsers(page));
        }
    })

    if (nextLink) {
        paginationNextBtn.setAttribute("onclick", `fetchUsers(${currentPage + 1})`);
        paginationNextBtn.classList.remove("disabled");
        paginationNextBtn.classList.add("enabled");
    }
    else {
        paginationNextBtn.removeAttribute("onclick");
        paginationNextBtn.classList.add("disabled");
        paginationNextBtn.classList.remove("enabled");
    }

    if (previousLink) {
        paginationBackBtn.setAttribute("onclick", `fetchUsers(${currentPage - 1})`);
        paginationBackBtn.classList.remove("disabled");
        paginationBackBtn.classList.add("enabled");
    }
    else {
        paginationBackBtn.removeAttribute("onclick");
        paginationBackBtn.classList.add("disabled");
        paginationBackBtn.classList.remove("enabled");
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
    generatePages(res.pagination.currentPage, res.pagination.total, res.pagination.links.previous, res.pagination.links.next);
    
    
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
