const paginationNextBtn = document.getElementById("pagination-next-btn");
const paginationBackBtn = document.getElementById("pagination-back-btn");

function fetchtokens(page) {
  console.log("Fetching page:", page);
  generatePages(Number(page), 10, page > 1, page < 10);
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
            span.addEventListener("click", () => fetchtokens(page));
        }
    })

    if (nextLink) {
        paginationNextBtn.setAttribute("onclick", `fetchtokens(${currentPage + 1})`);
        paginationNextBtn.classList.remove("disabled");
        paginationNextBtn.classList.add("enabled");
    }
    else {
        paginationNextBtn.removeAttribute("onclick");
        paginationNextBtn.classList.add("disabled");
        paginationNextBtn.classList.remove("enabled");
    }

    if (previousLink) {
        paginationBackBtn.setAttribute("onclick", `fetchtokens(${currentPage - 1})`);
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
                next: true
            },
            perPage: 10,
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



function applyFilter(filterParam) {
    activeFilter = filterParam;
    fetchtokens(1); // start from page 1 when a new filter is applied
}

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


fetchtokens(10);
