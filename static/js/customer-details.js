
let customer_id = JSON.parse(document.getElementById("customerId").textContent) || null;
let customers_data = null
let principle_data = null;
let customer_enndpoint = `${API_BASE_URL}customers/${customer_id}`;
window.addEventListener('load', get_customers_data(), get_principle_data());

async function get_customers_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI(customer_enndpoint, null, headers, 'GET');
        response.json().then(function(res) {
            if (response.status == 200) {
                customers_data = res.data;
                render_customers_data(res.data);
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

function render_customers_data(data) {
    if (customers_data){
        document.getElementById("name").textContent = data.user.name || "--";
        document.getElementById("email").textContent = data.user.email || "--";
        document.getElementById("address").textContent = data.address || "--";
        document.getElementById("city").textContent = data.city || "--";
        document.getElementById("state").textContent = data.state || "--";
        document.getElementById("zip").textContent = data.zip || "--";
        if(data.house_image){
            document.getElementById("house_image").src = data?.house_image;
        }
    } 
}

function principleDetails(principleId){
    sessionStorage.setItem("customer_id", customer_id)
    location.href = `/principle/details/${principleId}`;
}

async function get_principle_data(){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let enndpoint = `${API_BASE_URL}principles`
        let response = await requestAPI(enndpoint, null, headers, 'GET');
        response.json().then(function(res) {
            if (response.status == 200) {
                principle_data = res.data;
                attachItemListeners(principle_data);
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

function attachItemListeners(data) {
    const items = document.querySelectorAll(".energy-item");
    items.forEach((item, index)=> {
        let icon = item.querySelector(".icon");
        icon.addEventListener("click", function () {
            sessionStorage.setItem("customer_id", customer_id)
            location.href = `/principle/details/${data[index].id}`;
        });
    });
}
