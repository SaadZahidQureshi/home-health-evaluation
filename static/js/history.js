let customer_enndpoint = `${API_BASE_URL}customers`;
let customers_data = []
window.addEventListener('load', get_customers_data());

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
                render_customers_data(res);
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
    let container = document.querySelector("#customers-container");
    container.innerHTML = '';
    
    if (data.data.length == 0){
        console.log("no cutomers")
    }else{
        data.data.forEach(customer => {
            container.innerHTML += `
                <tr>
                    <td>${customer?.id || "--"}</td>
                    <td>${customer?.name || "--"}</td>
                    <td>${customer?.email || "--"}</td>
                    <td>${customer?.phone || "--"}</td>
                    <td>${customer?.address || "--"}</td>
                    <td>${customer?.created_at || "--"}</td>
                    <td>
                        <div class="action_button">
                            <a href="javascript:void(0)" onclick="deleteCustomer(${customer?.id})">
                                <img src="/static/img/delete-rounded.svg" alt="">
                            </a>
                            <a href="javascript:void(0)" onclick="editCustomer(${customer?.id})">
                                <img src="/static/img/edit-rounded.svg" alt="">
                            </a>
                        </div>
                    </td>
                </tr>`
        });
    }   
}

async function deleteCustomer(id){
    try {
        let headers = {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        };
        let response = await requestAPI( `${API_BASE_URL}customers/${id}`, null, headers, 'DELETE');
        if (response.status == 204) {
            let stored_id = sessionStorage.getItem("customer_id");
            if (stored_id == id) localStorage.removeItem("customer_id");
            showToast("Success", `Customer deleted successfully!`, "success-toast");
            get_customers_data();
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

function editCustomer(id){
    sessionStorage.setItem("customer_id", id);
    location.href = "/keep-it-clean/";
}