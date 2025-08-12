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
        container.innerHTML += `
                <tr >
                    <td colspan="6">No data available.</td>
                </tr>`
    }else{
        data.data.forEach(customer => {
            container.innerHTML += `
                <tr>
                    <td>${customer?.id || "--"}</td>
                    <td>${customer?.user?.name || "--"}</td>
                    <td>${customer?.user?.email || "--"}</td>
                    <td>${customer?.address || "--"}</td>
                    <td>${formatDate(customer?.created_at )|| "--"}</td>
                    <td>
                        <div class="action_button">
                            <a href="javascript:void(0)" onclick="deleteCustomer(${customer?.id})">
                                <img src="/static/img/delete-rounded.svg" alt="">
                            </a>
                            <a href="javascript:void(0)" onclick="editCustomer(${customer?.id})">
                                <img src="/static/img/edit-rounded.svg" alt="">
                            </a>
                            <a href="javascript:void(0)" onclick="viewCustomer(${customer?.id})">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="12" cy="12" r="3.3" stroke="#71BF1E" stroke-width="1.4"/>
                                    <path d="M20.188 10.9343C20.5762 11.4056 20.7703 11.6412 20.7703 12C20.7703 12.3588 20.5762 12.5944 20.188 13.0657C18.7679 14.7899 15.6357 18 12 18C8.36427 18 5.23206 14.7899 3.81197 13.0657C3.42381 12.5944 3.22973 12.3588 3.22973 12C3.22973 11.6412 3.42381 11.4056 3.81197 10.9343C5.23206 9.21014 8.36427 6 12 6C15.6357 6 18.7679 9.21014 20.188 10.9343Z" stroke="#71BF1E" stroke-width="1.7"/>
                                </svg>
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

function viewCustomer(id){
    location.href = `/saved/${id}`
}